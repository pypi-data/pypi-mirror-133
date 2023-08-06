// small word of warning - not the most beautiful code ever, sorry
// first goals is to get everything working
import { iterator, parse } from '@humanwhocodes/momoa';
import { loader } from '@monaco-editor/react';
import { options } from './custom-monaco-options';

let lastCacheKey = '';
let cachedAggIds: any[] = [];
let cachedPayloads: any[] = [];
const schemaDocumentationCache: Record<string, any> = {};

type NamespaceData = {
  title: string;
  types: { name: string; version: number }[];
};

loader.init().then(async (monaco) => {
  fetch(`/api/registry/namespaces?with-types=true`)
    .then(async (res) => {
      if (!res.ok) throw await res.json();

      const data: Record<string, NamespaceData> = await res.json();

      const namespaces = Object.keys(data);

      const anyOf: any[] = [];

      namespaces.forEach((namespace) => {
        const nsData = data[namespace];
        nsData.types.forEach((type) => {
          anyOf.push({
            type: 'object',
            properties: {
              ns: { description: nsData.title, enum: [namespace] },
              type: { enum: [type.name] },
              version: { enum: [type.version] },
            },
          });
        });
      });

      monaco.languages.json.jsonDefaults.setDiagnosticsOptions({
        validate: true,
        trailingCommas: 'ignore',
        allowComments: true,
        schemas: [
          {
            uri: 'http://fact-explorer/header-schema.json',
            fileMatch: ['header.json'],
            schema: {
              type: 'object',
              properties: {
                id: {
                  type: 'string',
                },
                aggIds: {
                  type: 'array',
                  items: {
                    type: 'string',
                  },
                },
                ns: { enum: namespaces },
                type: {
                  type: 'string',
                },
                version: {
                  type: 'integer',
                },
              },
              anyOf,
            },
          },
        ],
      });
    })
    .catch((error) => {
      console.error('Could not fetch namespaces with types from registry.');
      console.error(error);
    });

  const focusCommandId = 'fact-explorer.focusAggId';
  const mergeCommandId = 'fact-explorer.mergeAggId';

  monaco.editor.registerCommand(focusCommandId, (ctx, args) => {
    if (options.onFocusAggId) {
      options.onFocusAggId?.(args.aggId);
    } else {
      alert(`Command "${focusCommandId}" is not handled correctly.`);
    }
  });

  monaco.editor.registerCommand(mergeCommandId, (ctx, args) => {
    if (options.onMergeAggId) {
      options.onMergeAggId?.(args.aggId);
    } else {
      alert(`Command "${focusCommandId}" is not handled correctly.`);
    }
  });

  monaco.languages.registerHoverProvider('json', {
    provideHover(model, position) {
      if (model.uri.path !== '/result.json') return;

      // get agg ids (from cache if possible)
      const cacheKey = `${model.id}-${model.getVersionId()}`;
      if (cacheKey !== lastCacheKey) {
        const ast = parse(model.getValue());
        const aggIds: any[] = [];
        const payloads: any[] = [];
        for (const { node, parent, phase } of iterator(
          ast,
          ({ phase }: any) => phase === 'enter'
        )) {
          if (
            node.type === 'Member' &&
            node.name.value === 'aggIds' &&
            node.value.type === 'Array'
          ) {
            const ids = node.value.elements.filter(
              (element: any) => element.type === 'String'
            );
            aggIds.push(...ids);
          }
          if (
            node.type === 'Object' &&
            node.members.length === 2 &&
            node.members[0].name.value === 'header' &&
            node.members[1].name.value === 'payload'
          ) {
            const [headerNode, payloadNode] = node.members;
            const ns = headerNode.value.members.find(
              (member: any) => member.name.value === 'ns'
            ).value.value;
            const type = headerNode.value.members.find(
              (member: any) => member.name.value === 'type'
            ).value.value;
            const version = headerNode.value.members.find(
              (member: any) => member.name.value === 'version'
            ).value.value;
            payloads.push({ node: payloadNode, ns, type, version });
          }
        }
        lastCacheKey = cacheKey;
        cachedAggIds = aggIds;
        cachedPayloads = payloads;
      }

      // search agg id and provide hover
      const aggId = cachedAggIds.find(
        (aggId) =>
          aggId.loc.start.line === position.lineNumber &&
          aggId.loc.end.line === position.lineNumber &&
          aggId.loc.start.column <= position.column &&
          aggId.loc.end.column >= position.column
      );
      if (aggId) {
        const encodedArgs = encodeURIComponent(
          JSON.stringify({ aggId: aggId.value })
        );
        const focusLabel = 'Focus';
        const focusTooltip = 'Filter for this specific aggId.';
        const mergeLabel = 'Add to current filter';
        const mergeTooltip = 'Adds this specific aggId to the current filter.';

        return {
          range: new monaco.Range(
            aggId.loc.start.line,
            aggId.loc.start.column,
            aggId.loc.end.line,
            aggId.loc.end.column
          ),
          contents: [
            {
              value: `[${focusLabel}](command:${focusCommandId}?${encodedArgs} "${focusTooltip}") | [${mergeLabel}](command:${mergeCommandId}?${encodedArgs} "${mergeTooltip}")`,
              isTrusted: true,
            },
          ],
        };
      }

      // search payload and provide hover
      const payload = cachedPayloads.find(
        ({ node }) =>
          (node.loc.start.line < position.lineNumber ||
            (node.loc.start.line === position.lineNumber &&
              node.loc.start.column <= position.column)) &&
          (node.loc.end.line > position.lineNumber ||
            (node.loc.end.line === position.lineNumber &&
              node.loc.end.column >= position.column))
      );
      if (payload) {
        // possible future enhancement - cancel fetch, if no longer needed
        return getSchema(payload)
          .then((markdown) => {
            return {
              range: new monaco.Range(
                position.lineNumber,
                position.column,
                position.lineNumber,
                position.column
              ),
              contents: [
                {
                  value: markdown,
                  isTrusted: true,
                },
              ],
            };
          })
          .catch((error) => {
            console.error('Could not fetch schema from registry.');
            console.error(error);
            return null;
          });
      }

      return null;
    },
  });
});

async function getSchema({
  ns,
  type,
  version,
}: {
  ns: string;
  type: string;
  version: number;
}) {
  const params = `namespace=${ns}&type=${type}&version=${version}`;

  // use cache if possible
  if (schemaDocumentationCache[params]) return schemaDocumentationCache[params];

  const res = await fetch(
    `/api/registry/schema?namespace=${ns}&type=${type}&version=${version}`
  );

  if (!res.ok) throw await res.json();

  const schema = await res.json();
  let markdown = '';

  function forEachSchema(schema: any, depth = 0) {
    if (depth === 0 && schema.title) markdown += schema.title + `\n\n`;

    const props = schema.properties || schema.items.properties;
    if (props) {
      Object.keys(props).forEach((key) => {
        const prop = props[key];
        const isRequired = schema.required?.find(
          (item: string) => item === key
        );
        markdown +=
          (depth !== 0 ? ' '.repeat(depth * 2) + '- ' : '- ') +
          '**' +
          key +
          '**' +
          (isRequired ? ' _(required)_' : '') +
          `: \`{${prop.type}}\` ${prop.title ?? '_no description_'}\n\n`;
        if (prop.type === 'object') forEachSchema(prop, depth + 1);
        if (prop.type === 'array') forEachSchema(prop, depth + 1);
      });
    }
  }

  forEachSchema(schema);

  schemaDocumentationCache[params] = markdown;

  return markdown;
}

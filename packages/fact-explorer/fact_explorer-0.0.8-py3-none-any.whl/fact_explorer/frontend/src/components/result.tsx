import Editor from '@monaco-editor/react';
import type { editor } from 'monaco-editor/esm/vs/editor/editor.api';
import { useEffect, useState, VFC } from 'react';
import { FactOut } from '../types/types';

type FoldLevel = '1' | '2' | '3' | '4' | '5' | '6' | '7' | 'unfold';

export const Result: VFC<{
  data: FactOut[];
  path?: string;
}> = ({ data, path }) => {
  const [editor, setEditor] = useState<editor.IStandaloneCodeEditor | null>(
    null
  );

  const [foldLevel, setFoldLevel] = useState<FoldLevel>(
    () => (localStorage.getItem('editorFoldLevel') as FoldLevel | null) ?? '4'
  );

  useEffect(() => {
    if (!editor) return;
    localStorage.setItem('editorFoldLevel', foldLevel);
    editor.trigger('unfold', 'editor.unfoldAll', {});
    if (foldLevel === 'unfold') return;

    if (foldLevel === '1') editor.trigger('fold', 'editor.foldAll', {});
    else editor.trigger('fold', `editor.foldLevel${foldLevel}`, {});
  }, [foldLevel, editor]);

  if (!data.length)
    return (
      <div className="p-5 shadow-inner">
        <p>No result.</p>
      </div>
    );

  const value = JSON.stringify(data, null, 2);

  return (
    <>
      <div className="p-4">
        <label className="text-xs">
          Folding:{' '}
          <select
            className="focus:ring-blue-500 focus:border-blue-500 shadow-sm border border-gray-300 rounded-md p-0.5 text-xs"
            onChange={(e) => {
              const foldLevel = e.currentTarget.value;
              setFoldLevel(foldLevel as FoldLevel);
            }}
            value={foldLevel}
          >
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
            <option value="6">6</option>
            <option value="7">7</option>
            <option value="unfold">Unfold All</option>
          </select>
        </label>
      </div>

      <Editor
        path={path}
        height={600}
        defaultLanguage="json"
        value={value}
        options={{
          scrollBeyondLastLine: false,
          readOnly: true,
          minimap: { enabled: false },
          unusualLineTerminators: 'auto',
        }}
        onMount={(editor, monaco) => {
          setEditor(editor);

          // hide read-only tooltip
          // see https://github.com/microsoft/monaco-editor/issues/1742#issuecomment-998853901
          const messageContribution = editor.getContribution(
            'editor.contrib.messageController'
          );
          editor.onDidAttemptReadOnlyEdit(() => messageContribution.dispose());
        }}
      />
    </>
  );
};

import { yupResolver } from '@hookform/resolvers/yup';
import Editor from '@monaco-editor/react';
import type { editor } from 'monaco-editor/esm/vs/editor/editor.api';
import type { NextPage } from 'next';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import {
  Control,
  Controller,
  FieldPath,
  FieldValues,
  useForm,
} from 'react-hook-form';
import * as yup from 'yup';
import * as queryString from 'query-string';
import { Card } from '../components/card';
import { Form } from '../components/form';
import { Label } from '../components/label';
import { Result } from '../components/result';
import { Title } from '../components/title';
import { useFetch } from '../hooks/use-fetch';
import { useParams } from '../hooks/use-params';
import { useSubmit } from '../hooks/use-submit';
import { FactOut } from '../types/types';
import { options } from '../utils/custom-monaco-options';

const schema = yup
  .object({
    header: yup.string().defined(),
    payload: yup.string().defined(),
    skipResults: yup
      .number()
      .transform((value, originalValue) =>
        originalValue === '' ? undefined : value
      )
      .typeError('Results to Skip must be a number')
      .required()
      .integer()
      .min(0),
    maxResults: yup
      .number()
      .transform((value, originalValue) =>
        originalValue === '' ? undefined : value
      )
      .typeError('Max. Results must be a number')
      .required()
      .integer()
      .min(1)
      .max(1000),
    decrypt: yup.boolean().defined(),
  })
  .required();

type FormValues = yup.Asserts<typeof schema>;

const defaultFormValues: FormValues = {
  header: '{}',
  payload: '{}',
  skipResults: 0,
  maxResults: 20,
  decrypt: false,
};

const Home: NextPage = () => {
  const params = useParams(defaultFormValues);

  useEffect(() => {
    const query = queryString.stringify(params);
    search.execute(`/api/search?${query}`, {
      headers: { Accept: 'application/json' },
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params]);

  const {
    register,
    handleSubmit,
    formState: { errors },
    control,
    setValue,
    getValues,
  } = useForm<FormValues>({
    resolver: yupResolver(schema),
    defaultValues: params,
  });

  const search = useFetch<FactOut[]>();
  const submit = useSubmit();
  const router = useRouter();

  const onSubmit = handleSubmit(
    (values) => {
      router.push({ pathname: '/search', query: values });
    },
    (errors) => {
      submit.onError();
    }
  );

  useEffect(() => {
    options.onFocusAggId = (aggId) => {
      setValue('payload', '{}');
      setValue('header', JSON.stringify({ aggIds: [aggId] }, null, 2));
      onSubmit();
    };

    return () => {
      delete options.onFocusAggId;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    options.onMergeAggId = (aggId) => {
      setValue('payload', '{}');
      const header = JSON.parse(getValues('header'));
      const isHeaderObject =
        typeof header === 'object' && header !== null && !Array.isArray(header);
      setValue(
        'header',
        JSON.stringify(
          isHeaderObject
            ? {
                ...header,
                aggIds: Array.isArray(header.aggIds)
                  ? [...header.aggIds, aggId]
                  : [aggId],
              }
            : { aggIds: ['${aggId}'] },
          null,
          2
        )
      );
      onSubmit();
    };

    return () => {
      delete options.onMergeAggId;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <>
      <Head>
        <title>Search</title>
      </Head>

      <Title>Search</Title>

      <Card>
        <Form onSubmit={onSubmit}>
          <div>
            <EditorInput label="Header Query" control={control} name="header" />
            {errors.header && (
              <p className="text-sm text-red-500">⚠ {errors.header.message}</p>
            )}
          </div>

          <div>
            <EditorInput
              label="Payload Query"
              control={control}
              name="payload"
            />
            {errors.payload && (
              <p className="text-sm text-red-500">⚠ {errors.payload.message}</p>
            )}
          </div>

          <div>
            <Label htmlFor="skipResults">Number of Results to Skip</Label>
            <input
              id="skipResults"
              type="number"
              className=" focus:ring-blue-500 focus:border-blue-500 w-full shadow-sm border border-gray-300 rounded-md p-1"
              {...register('skipResults')}
            />
            {errors.skipResults && (
              <p className="text-sm text-red-500">
                ⚠ {errors.skipResults.message}
              </p>
            )}
          </div>

          <div>
            <Label htmlFor="maxResults">Max. Results to Return</Label>
            <input
              id="maxResults"
              type="number"
              className=" focus:ring-blue-500 focus:border-blue-500 w-full shadow-sm border border-gray-300 rounded-md p-1"
              {...register('maxResults')}
            />
            {errors.maxResults && (
              <p className="text-sm text-red-500">
                ⚠ {errors.maxResults.message}
              </p>
            )}
          </div>

          <label>
            <input type="checkbox" {...register('decrypt')} /> Decrypt Result
          </label>

          <div className="text-right">
            <button {...submit.props}>Get Events</button>
          </div>
        </Form>

        {search.loading ? (
          <div className="p-5 shadow-inner">
            <span className="inline-block animate-spin">↻</span> Loading...
          </div>
        ) : search.data ? (
          <Result data={search.data} path="result.json" />
        ) : null}
      </Card>
    </>
  );
};

function EditorInput<
  TFieldValues extends FieldValues = FieldValues,
  TName extends FieldPath<TFieldValues> = FieldPath<TFieldValues>
>({
  label,
  control,
  name,
}: {
  label: string;
  control: Control<TFieldValues>;
  name: TName;
}) {
  const [editor, setEditor] = useState<editor.IStandaloneCodeEditor | null>(
    null
  );
  return (
    <>
      <Label onClick={() => editor?.focus()}>{label}</Label>
      <Controller
        render={({ field }) => {
          const lines = (field.value.match(/\n/g) ?? []).length + 1;
          const lineHeight = 18;
          const height = lines * lineHeight;
          return (
            <div
              className="focus:ring-blue-500 focus:border-blue-500 w-full shadow-sm border border-gray-300 rounded-md p-1"
              style={{ height: height + 9 }}
            >
              <Editor
                loading={
                  <p className="w-full" style={{ paddingLeft: '26px' }}>
                    Loading...
                  </p>
                }
                path={`${name}.json`}
                height={height}
                defaultLanguage="json"
                value={field.value}
                onChange={(value) => {
                  field.onChange({ target: { value: value ?? '' } });
                }}
                options={{
                  lineNumbers: 'off',
                  scrollBeyondLastLine: false,
                  minimap: { enabled: false },
                  overviewRulerLanes: 0,
                  renderLineHighlight: 'none',
                }}
                onMount={(editor, monaco) => {
                  setEditor(editor);

                  // show suggestions docs by default? unsure about this
                  // see https://github.com/microsoft/monaco-editor/issues/2241#issuecomment-997339142
                  // let { widget } = editor.getContribution(
                  //   'editor.contrib.suggestController'
                  // );
                  // if (widget) {
                  //   const suggestWidget = widget.value;
                  //   if (suggestWidget && suggestWidget._setDetailsVisible) {
                  //     // default to visible details
                  //     suggestWidget._setDetailsVisible(true);
                  //   }
                  //   if (suggestWidget && suggestWidget._persistedSize) {
                  //     suggestWidget._persistedSize.store({
                  //       width: 500,
                  //       height: 600,
                  //     });
                  //   }
                  // }
                }}
              />
            </div>
          );
        }}
        control={control}
        name={name}
      />
    </>
  );
}

export default Home;

import { yupResolver } from '@hookform/resolvers/yup';
import type { NextPage } from 'next';
import Head from 'next/head';
import { useEffect } from 'react';
import { useForm } from 'react-hook-form';
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
import { useRouter } from 'next/router';

const schema = yup
  .object({
    minutes: yup
      .number()
      .transform((value, originalValue) =>
        originalValue === '' ? undefined : value
      )
      .typeError('minutes must be a number')
      .required()
      .integer()
      .min(1)
      .max(60),
    decrypt: yup.boolean().defined(),
  })
  .required();

type FormValues = yup.Asserts<typeof schema>;

const defaultFormValues: FormValues = {
  minutes: 15,
  decrypt: false,
};

const Home: NextPage = () => {
  const params = useParams(defaultFormValues);

  useEffect(() => {
    const query = queryString.stringify(params);
    lastMinutes.execute(`/api/last?${query}`, {
      headers: { Accept: 'application/json' },
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params]);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: yupResolver(schema),
    defaultValues: params,
  });

  const lastMinutes = useFetch<FactOut[]>();
  const submit = useSubmit();
  const router = useRouter();

  const onSubmit = handleSubmit(
    (values) => {
      router.push({ pathname: '/', query: values });
    },
    (errors) => {
      submit.onError();
    }
  );

  return (
    <>
      <Head>
        <title>Last Minutes</title>
      </Head>

      <Title>Retrieve Events from Last Minutes</Title>

      <Card>
        <Form onSubmit={onSubmit}>
          <div>
            <Label htmlFor="minutes">Minutes</Label>
            <input
              id="minutes"
              type="number"
              className=" focus:ring-blue-500 focus:border-blue-500 w-full shadow-sm border border-gray-300 rounded-md p-1"
              {...register('minutes')}
            />
            {errors.minutes && (
              <p className="text-sm text-red-500">⚠ {errors.minutes.message}</p>
            )}
          </div>

          <label>
            <input type="checkbox" {...register('decrypt')} /> Decrypt Result
          </label>

          <div className="text-right">
            <button {...submit.props}>Get Events</button>
          </div>
        </Form>

        {lastMinutes.loading ? (
          <div className="p-5 shadow-inner">
            <span className="inline-block animate-spin">↻</span> Loading...
          </div>
        ) : lastMinutes.data ? (
          <Result data={lastMinutes.data} />
        ) : null}
      </Card>
    </>
  );
};

export default Home;

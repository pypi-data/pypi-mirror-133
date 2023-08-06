import type { NextPage } from 'next';
import Head from 'next/head';
import { Title } from '../components/title';

const NotFound: NextPage = () => {
  return (
    <>
      <Head>
        <title>Not Found</title>
      </Head>

      <Title>Not Found</Title>

      <p>404: We couldn&apos;t find the page.</p>
    </>
  );
};

export default NotFound;

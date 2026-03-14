import { ApolloClient, InMemoryCache } from '@apollo/client';
import UploadHttpLink from 'apollo-upload-client/UploadHttpLink.mjs';

const uploadLink = new UploadHttpLink({
  uri: 'http://127.0.0.1:5000/graphql',
});

export const client = new ApolloClient({
  link: uploadLink,
  cache: new InMemoryCache(),
});


// import { ApolloClient, InMemoryCache, HttpLink } from '@apollo/client';
// const httpLink = new HttpLink({
//   uri: 'http://127.0.0.1:5000/graphql',
// });

// export const client = new ApolloClient({
//   link: httpLink,
//   cache: new InMemoryCache(),
// });

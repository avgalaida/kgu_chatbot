import './assets/main.css'

import { ApolloClient, createHttpLink, InMemoryCache } from '@apollo/client/core'

// HTTP connection to the API
const httpLink = createHttpLink({
    // You should use an absolute URL here
    uri: 'http://127.0.0.1:8000/graphql',
})

// Cache implementation
const cache = new InMemoryCache()

// Create the apollo client
const apolloClient = new ApolloClient({
    link: httpLink,
    cache,
})

import { createApolloProvider } from '@vue/apollo-option'

const apolloProvider = createApolloProvider({
    defaultClient: apolloClient,
})

import { createApp } from 'vue'
import App from './App.vue'

createApp(App).use(apolloProvider).mount('#app')

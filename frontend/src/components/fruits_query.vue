<template>
  <div>
    <h1>hello</h1>
    <li v-for="fruit in fruits" :key="fruit.id">{{ fruit.name }}</li>
  </div>
</template>

<script>
import gql from 'graphql-tag';

export default {
  apollo: {
    fruits: {
      query: gql`
        query {
          fruits {
            id
            name
            color
          }
        }
      }`
    },
  },
};
</script>

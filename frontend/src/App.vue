<template>
  <div class="centered-content">
    <div class="chat-input">
      <h2 style="text-align: center" >КГУ QA</h2>
      <ChatInput/>
    </div>
  </div>
</template>

<script setup>
import ChatInput from "@/components/ChatInput.vue";
</script>

<style scoped>
.centered-content {
  display: flex;
  justify-content: center; /* Выравнивание по горизонтали */
  align-items: center; /* Выравнивание по вертикали */
  height: 100vh; /* Для центрирования по всей высоте экрана */
}

/* Ваши стили для .chat-input, если есть */
.chat-input {
  /* Ваши стили */
}
</style>

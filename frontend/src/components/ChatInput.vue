<template>
  <div class="apollo">
    <div class="message-history" ref="messageHistoryRef">
      <div
          v-for="(message, index) in messageHistory"
          :key="index"
          :class="{ 'user-message': isUserMessage(message), 'server-message': !isUserMessage(message), 'new-message': index >= messageHistory.length - newMessageCount }"
      >
        <p>{{ message }}</p>
      </div>
      <div>
        <img v-if="image !== 'None'" :src="image" alt="Изображение">
      </div>
<!--      <audio autoplay="autoplay" controls="controls" preload="auto" ref="audio">-->
<!--        <source-->
<!--            src={{audio}}-->
<!--            type="audio/mpeg"-->
<!--        >-->
<!--      </audio>-->
    </div>
    <div class="message-input">
      <input
          v-model="text"
          placeholder="Задайте вопрос"
          class="input-field"
      />
      <button @click="sendMessage" class="custom-send-button">
        Отправить
      </button>
      <button @click="handleRecording" class="custom-send-button">
        <svg @click.stop="handleRecording" width="18" height="18" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
          <g clip-path="url(#clip0_122_101)">
            <path fill="white" d="M8.99998 2.25C8.40325 2.25 7.83095 2.48705 7.40899 2.90901C6.98703 3.33097 6.74998 3.90326 6.74998 4.5V9C6.74998 9.59674 6.98703 10.169 7.40899 10.591C7.83095 11.0129 8.40325 11.25 8.99998 11.25C9.59672 11.25 10.169 11.0129 10.591 10.591C11.0129 10.169 11.25 9.59674 11.25 9V4.5C11.25 3.90326 11.0129 3.33097 10.591 2.90901C10.169 2.48705 9.59672 2.25 8.99998 2.25ZM8.99998 0.75C9.49244 0.75 9.98007 0.846997 10.435 1.03545C10.89 1.22391 11.3034 1.50013 11.6516 1.84835C11.9999 2.19657 12.2761 2.60997 12.4645 3.06494C12.653 3.51991 12.75 4.00754 12.75 4.5V9C12.75 9.99456 12.3549 10.9484 11.6516 11.6517C10.9484 12.3549 9.99454 12.75 8.99998 12.75C8.00542 12.75 7.05159 12.3549 6.34833 11.6517C5.64507 10.9484 5.24998 9.99456 5.24998 9V4.5C5.24998 3.50544 5.64507 2.55161 6.34833 1.84835C7.05159 1.14509 8.00542 0.75 8.99998 0.75ZM1.64398 10.4715L3.11548 10.1768C3.38877 11.5361 4.12425 12.7589 5.19696 13.6374C6.26967 14.5159 7.61345 14.9959 8.99998 14.9959C10.3865 14.9959 11.7303 14.5159 12.803 13.6374C13.8757 12.7589 14.6112 11.5361 14.8845 10.1768L16.356 10.4715C15.672 13.9088 12.6375 16.5 8.99998 16.5C5.36248 16.5 2.32798 13.9088 1.64398 10.4715Z"/>
          </g>
          <defs>
            <clipPath id="clip0_122_101">
              <rect width="18" height="18" fill="white"/>
            </clipPath>
          </defs>
        </svg>
      </button>
    </div>
  </div>
</template>

<script>
import gql from 'graphql-tag';

export default {
  data() {
    return {
      text: '',
      response: '',
      messageHistory: [], // Массив для хранения истории сообщений
      newMessageCount: 0, // Счетчик новых сообщений
      // Данные для функции записи аудио
      mediaRecorder: null,
      audioChunks: [],
      recording: false, // Переменная состояния для записи/остановки
      image: 'None',
      audio: null
    };
  },
  methods: {
    generateSpeech(t){
      this.$apollo
          .mutate({
            mutation: gql`
              mutation GenerateSpeech($text: String!, $speaker: String! ) {
                generateSpeech(text: $text, speaker: $speaker)
              }
            `,
            variables: {
              text: t,
              speaker: 'baya'
            },
          })
          .then((result) => {
            const base64string = result.data.generateSpeech;
            const snd = new Audio("data:audio/wav;base64," + base64string);
            snd.play();
            console.log(snd)
          })
          .catch((error) => {
            console.error(error);
          });
    },
    sendMessage() {
      if (this.text.trim() !== '') {
        this.messageHistory.push(`Вы: ${this.text}`);

        this.$apollo
            .query({
              query: gql`
              query respond($text: String!) {
                respond(text: $text)
              }
            `,
              variables: {
                text: this.text,
              },
            })
            .then((result) => {
              this.response = result.data.respond;
              this.ans = this.response[0]
              this.image = this.response[1]
              this.messageHistory.push(`Сервер: ${this.ans}`);
              this.text = '';
              this.newMessageCount++;
              this.scrollMessageHistory();
              this.generateSpeech(this.ans)
            })
            .catch((error) => {
              console.error(error);
            });
      }
    },
    isUserMessage(message) {
      return message.startsWith('Вы:');
    },
    scrollMessageHistory() {
      this.$nextTick(() => {
        const messageHistory = this.$refs.messageHistoryRef;
        messageHistory.scrollTop = messageHistory.scrollHeight;
      });
    },
    handleRecording() {
      if (!this.recording) {
        this.startRecording();
      } else {
        this.stopRecording();
      }
    },
    async startRecording() {
      await this.uploadAudio();

      // const constraints = {
      //   audio: {
      //     sampleRate: 16000, // Задаем желаемый семпл-рейт
      //     // Другие настройки, если нужны
      //   }
      // };
      // const stream = await navigator.mediaDevices.getUserMedia(constraints);
      // this.mediaRecorder = new MediaRecorder(stream);
      // this.mediaRecorder.ondataavailable = (e) => {
      //   console.log('Data available:', e.data.size);
      //   this.audioChunks.push(e.data)
      // };
      // this.mediaRecorder.start(1000);
      this.recording = true;
      this.recording = false;
    },
    // stopRecording() {
    //   // this.mediaRecorder.stop();
    //   // this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
    //   // this.recording = false;
    // },
    async uploadAudio() {
      // const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
      // const audioBuffer = await audioBlob.arrayBuffer();
      // const base64Audio = btoa(String.fromCharCode(...new Uint8Array(audioBuffer)));
      // console.log('b64: ', base64Audio)
      const base64Audio = ""

      const UPLOAD_AUDIO_MUTATION = gql`
        mutation UploadAudio($audioData: String!) {
          uploadAudio(audioData: $audioData)
        }
      `;

      this.$apollo.mutate({
        mutation: UPLOAD_AUDIO_MUTATION,
        variables: {
          audioData: base64Audio
        }
      }).then(response => {
        this.text = response.data.uploadAudio;
        console.log("Аудио успешно загружено:", response.data.uploadAudio);
        this.sendMessage()
      }).catch(error => {
        console.error("Ошибка при загрузке аудио:", error);
      });
    },
  },
};
</script>

<style scoped>
/* Стили для отображения разных типов сообщений */
.message-history {
  margin-bottom: 10px;
}

.user-message {
  text-align: right;
  margin: 5px 20px;
  background-color: #C571F8;
  border-radius: 8px;
  padding: 8px;
  color: #FFFFFF;
}

.server-message {
  text-align: left;
  margin: 5px 20px;
  background-color: #E0E0E0;
  border-radius: 8px;
  padding: 8px;
  color: #000;
}

/* Новые стили для поля ввода сообщения и кнопок */
.message-input {
  display: flex;
  align-items: center;
}

.input-field {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 10px;
  font-size: 16px;
}

.custom-send-button {
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  background-color: #C571F8;
  color: #FFFFFF;
  font-size: 16px;
  cursor: pointer;
}

.custom-send-button:hover {
  background-color: #9150E3;
}

/* Анимация для новых сообщений */
.new-message {
  animation-name: fadeIn;
  animation-duration: 0.5s;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

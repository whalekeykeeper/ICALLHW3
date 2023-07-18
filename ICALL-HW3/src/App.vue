<script>
import axios from 'axios';

export default {
  data() {
    return {
      textInput: '',
      selectedTagType: 'POS',
      tags: [],
      tagColors: {},
      processedText: '',
      highlightedText: '',
      process_base: 'http://127.0.0.1:5000',
    };
  },
  methods: {
    submitForm() {
      axios
          .post(this.process_base + '/process-text', {
            text: this.textInput,
            [this.selectedTagType]: true,
          })
          .then((response) => {
            this.tags = response.data.tags;
            this.initializeTagColors();
            this.processedText = response.data.highlightedText; // Store processed text
            this.applyHighlighting(); // Call applyHighlighting after setting processedText
          })
          .catch((error) => {
            console.error(error);
          });
    },
    applyHighlighting() {
      let highlightedText = this.processedText || this.textInput;
      for (const [tag, color] of Object.entries(this.tagColors)) {
        highlightedText = highlightedText.replace(
            new RegExp(`<${tag}>`, 'g'),
            `<span style="background-color: ${color}">`,
        );
        highlightedText = highlightedText.replace(
            new RegExp(`</${tag}>`, 'g'),
            '</span>',
        );
      }
      
      this.highlightedText = highlightedText;
    },
    initializeTagColors() {
      const randomColor = () => "#" + Math.floor(Math.random() * 16777215).toString(16);

      for (const tag of this.tags) {
        this.tagColors[tag] = randomColor();
      }
    },
  },
};
</script>

<template>
  <div>
    <form @submit.prevent="submitForm">
      <textarea v-model="textInput" rows="5" cols="40"></textarea>
      <div>
        <label>
          Highlight:
          <select v-model="selectedTagType">
            <option value="POS">Part-of-Speech (POS) Tags</option>
            <option value="NE">Named Entity (NE) Tags</option>
          </select>
        </label>
      </div>
      <div>
        <div v-for="(tag, index) in tags" :key="index">
          <input type="color" v-model="tagColors[tag]" @input="applyHighlighting" />
          {{ tag }}
        </div>
      </div>
      <button type="submit">Submit</button>
    </form>
    <div>
      <br><br>
      <p v-html="highlightedText"></p>
    </div>
  </div>
</template>


<style scoped>
textarea {
  width: 100%;
  margin-bottom: 10px;
}

input[type="color"] {
  vertical-align: middle;
  margin-right: 5px;
}
</style>

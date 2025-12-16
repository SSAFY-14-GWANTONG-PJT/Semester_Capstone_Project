<template>
  <div class="write-page">
    <h2>글 작성</h2>

    <form @submit.prevent="submit">
      <input v-model="form.title" placeholder="제목" />
      <textarea v-model="form.content" placeholder="내용"></textarea>

      <select v-model="form.status">
        <option value="review">학습 후기</option>
        <option value="question">질문</option>
      </select>

      <button type="submit">등록</button>
    </form>
  </div>
</template>

<script setup>
import { reactive } from "vue";

const form = reactive({
  title: "",
  content: "",
  status: "review",
});

const submit = async () => {
  // POST /posts 연동
  console.log("submit", form);
};
</script>
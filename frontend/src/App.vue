<template>
  <div id="app">
    <router-view />
    <!-- 🔥 Render nội dung các trang -->
    <ChatBot v-if="showChatBot" />
    <!-- ✅ ChatBot luôn tồn tại -->
  </div>
</template>

<script>
import ChatBot from "@/views/ChatBot.vue";
export default {
  components: { ChatBot },
  computed: {
    showChatBot() {
      // Ẩn ChatBot ở /login và /register
      return !["/login", "/register"].includes(this.$route.path);
    }
  }
};
</script>

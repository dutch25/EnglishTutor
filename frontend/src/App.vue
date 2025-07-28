<template>
  <div id="app">
    <router-view />
    <!-- 🔥 Render nội dung các trang -->
    <ChatBot />
    <!-- ✅ ChatBot luôn tồn tại -->
  </div>
</template>

<script>
import ChatBot from "@/views/ChatBot.vue";
export default {
  components: { ChatBot },
};
</script>

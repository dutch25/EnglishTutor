<template>
  <div>
    <div
      class="chat-bubble"
      :style="{ transform: `translate(${bubblePos.x}px, ${bubblePos.y}px)` }"
      @mousedown="handleBubbleMouseDown"
      @click="toggleChat"
    >
      <img :src="messengerIcon" alt="Chat" />
    </div>

    <div
      v-if="showChat"
      class="chat-window"
      :style="{
        transform: `translate(${chatPos.x}px, ${chatPos.y}px)`,
        width: chatSize.width + 'px',
        height: chatSize.height + 'px',
      }"
    >
      <div class="chat-header" @mousedown="startWindowDrag">
        <span>EngAI Bot</span>
        <button @click.stop="closeChat">✖</button>
      </div>

      <div class="chat-body">
        <div
          v-for="(msg, i) in messages"
          :key="i"
          :class="['chat-msg', msg.sender]"
          v-html="msg.html"
        ></div>
        <div
        v-for="(msg, i) in messages2"
        :key="i"
        :class="['chat-msg', msg.sender]"
        v-html="msg.html"
        ></div>

        <div v-if="typing" class="typing-indicator bot">
          <span></span><span></span><span></span>
        </div>
      </div>

      <div class="chat-footer">
        <input
          v-model="userMessage"
          type="text"
          placeholder="Nhập tin nhắn..."
          @keyup.enter="sendMessage"
        />
        <button @click="sendMessage">Gửi</button>
      </div>

      <div class="resize-handle" @mousedown.stop="startResize"></div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { marked } from "marked";
import chatbotIcon from "@/assets/Chatbot.png";

export default {
  name: "ChatBot",
  data() {
    return {
      messengerIcon: chatbotIcon,
      showChat: false,
      bubblePos: { x: 0, y: 0 },
      chatPos: { x: 0, y: -100 },
      chatSize: { width: 320, height: 400 },
      isDragging: false,
      isAnimating: false,
      userMessage: "",
      messages: [
        { sender: "bot", html: "Chào mừng bạn đến với nền tảng học English trực tuyến EngAI!" },
      ],
      messages2:[
        { sender: "bot", html: "Tôi có thể giúp gì cho bạn!" },
      ],
      typing: false,
      drag: { target: null, offsetX: 0, offsetY: 0 },
      resize: { active: false, startX: 0, startY: 0, startW: 320, startH: 400 },
      isDragging: false,
    };
  },
  mounted() {
    this.showChat = localStorage.getItem("chat_open") === "true";
    this.bubblePos = { x: 0, y: 0 };  // Khởi đầu không cần set toạ độ tuyệt đối.
  },
  methods: {
    closeChat() {
      this.showChat = false;
      localStorage.setItem("chat_open", "false");
    },
    toggleChat() {
      this.showChat = !this.showChat;
      localStorage.setItem("chat_open", this.showChat);
    },

    handleBubbleMouseDown(e) {
  if (this.isAnimating) return;
  e.preventDefault();
  this.isDragging = true;
  this.drag.offsetX = e.clientX - this.bubblePos.x;
  this.drag.offsetY = e.clientY - this.bubblePos.y;

  const onMouseMove = (ev) => {
    if (!this.isDragging) return;
    this.bubblePos.x = ev.clientX - this.drag.offsetX;
    this.bubblePos.y = ev.clientY - this.drag.offsetY;
  };

  const onMouseUp = () => {
    if (!this.isDragging) return;
    this.isDragging = false;
    document.removeEventListener("mousemove", onMouseMove);
    document.removeEventListener("mouseup", onMouseUp);
    this.snapBubbleToEdge();
  };

  document.addEventListener("mousemove", onMouseMove);
  document.addEventListener("mouseup", onMouseUp);
},

    snapBubbleToEdge() {
  const screenWidth = window.innerWidth;
  const screenHeight = window.innerHeight;
  const bubbleWidth = 60;
  const bubbleHeight = 60;
  const edgeMargin = 20;

  // Tính toạ độ hiện tại (translate)
  const currentLeft = 20 + this.bubblePos.x + bubbleWidth / 2;

  // Xác định snap sang trái hay phải
  const snapToRight = currentLeft >= screenWidth / 2;

  const targetX = snapToRight
    ? screenWidth - bubbleWidth - edgeMargin * 2 - 20 - 20 // Cân chỉnh chuẩn lề phải
    : 0;

  // Y tính như cũ
  let targetY = this.bubblePos.y;
  const minY = -(screenHeight - bubbleHeight - edgeMargin * 2);
  const maxY = 0;
  targetY = Math.min(Math.max(targetY, minY), maxY);

  // Snap
  this.isAnimating = true;
  this.bubblePos = { x: targetX, y: targetY };

  setTimeout(() => {
    this.isAnimating = false;
  }, 300);
},

    startWindowDrag(e) {
      e.stopPropagation();
      this.drag.target = "chat";
      this.drag.offsetX = e.clientX - this.chatPos.x;
      this.drag.offsetY = e.clientY - this.chatPos.y;
      document.addEventListener("mousemove", this.onDrag);
      document.addEventListener("mouseup", this.stopDrag);
    },
    onDrag(e) {
      if (this.drag.target === "chat") {
        this.chatPos.x = e.clientX - this.drag.offsetX;
        this.chatPos.y = e.clientY - this.drag.offsetY;
      } else if (this.resize.active) {
        this.chatSize.width = Math.max(
          250,
          this.resize.startW + (e.clientX - this.resize.startX)
        );
        this.chatSize.height = Math.max(
          250,
          this.resize.startH + (e.clientY - this.resize.startY)
        );
      }
    },
    stopDrag() {
      this.drag.target = null;
      this.resize.active = false;
      document.removeEventListener("mousemove", this.onDrag);
      document.removeEventListener("mouseup", this.stopDrag);
    },
    startResize(e) {
      this.resize.active = true;
      this.resize.startX = e.clientX;
      this.resize.startY = e.clientY;
      this.resize.startW = this.chatSize.width;
      this.resize.startH = this.chatSize.height;
      document.addEventListener("mousemove", this.onDrag);
      document.addEventListener("mouseup", this.stopDrag);
    },

    async sendMessage() {
      if (!this.userMessage.trim()) return;

      this.messages.push({ sender: "user", html: this.userMessage });
      const msg = this.userMessage;
      this.userMessage = "";
      this.typing = true;

      try {
        const res = await axios.post("http://127.0.0.1:8000/chat", {
          message: msg,
        });
        const reply = res.data.reply || "Bot không phản hồi.";
        this.messages.push({ sender: "bot", html: marked(reply) });
      } catch {
        this.messages.push({ sender: "bot", html: "⚠️ Lỗi kết nối server!" });
      } finally {
        this.typing = false;
      }
    },
  },
};
</script>

<style scoped>
/* 🔵 Bubble */
.chat-bubble {
  position: fixed;
  left: 20px;
  top: auto;
  bottom: 20px;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: grab;
  z-index: 9999;
  transition: transform 0.3s ease;
}

.chat-bubble img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: transparent; /* ✅ tạo nền trắng nếu icon trong suốt */
  padding: 5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.2s;
}
.chat-bubble img:hover {
  transform: scale(1.1); /* ✅ hiệu ứng hover */
}

/* 💬 Window */
.chat-window {
  position: fixed;
  bottom: 100px;
  right: 30px;
  background: #2a2a3d;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
  z-index: 9999;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.chat-header {
  background: #db89eb;
  padding: 10px;
  color: white;
  display: flex;
  justify-content: space-between;
  cursor: grab;
}
.chat-body {
  flex: 1;
  padding: 10px;
  color: #ddd;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

/* 💬 Messenger Style */
.chat-msg {
  max-width: 75%;
  padding: 8px 12px;
  border-radius: 16px;
  word-wrap: break-word;
  line-height: 1.4;
}
.chat-msg.user {
  background: #0084ff;
  color: white;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}
.chat-msg.bot {
  background: #3a3a4d;
  color: white;
  align-self: flex-start;
  border-bottom-left-radius: 4px;
}

/* Typing Indicator */
.typing-indicator {
  background: #3a3a4d;
  padding: 6px 10px;
  border-radius: 12px;
  display: flex;
  gap: 4px;
  width: fit-content;
}
.typing-indicator span {
  width: 6px;
  height: 6px;
  background: white;
  border-radius: 50%;
  animation: blink 1.4s infinite;
}
.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}
.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}
@keyframes blink {
  0%,
  80%,
  100% {
    opacity: 0.3;
    transform: scale(0.7);
  }
  40% {
    opacity: 1;
    transform: scale(1);
  }
}

.chat-footer {
  display: flex;
  padding: 10px;
  gap: 5px;
}
.chat-footer input {
  flex: 1;
  padding: 5px;
  border-radius: 4px;
  border: none;
}
.chat-footer button {
  background: #0084ff;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
}

/* Resize handle */
.resize-handle {
  position: absolute;
  width: 15px;
  height: 15px;
  right: 2px;
  bottom: 2px;
  background: rgba(255, 255, 255, 0.3);
  cursor: se-resize;
  border-radius: 3px;
}
</style>

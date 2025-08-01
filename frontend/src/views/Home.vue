<template>
  <div class="app-wrapper">
    <!-- Header -->
    <div class="header-section">
      <div class="title-container">
        <img :src="logoUrl" alt="English Tutor" class="logo" />
        <div class="text-title">
          <h1 class="title">English Tutor</h1>
        </div>
      </div>
    </div>

    <!-- Grid Features -->
    <div class="feature-grid">
      <div
        v-for="item in features"
        :key="item.title"
        class="feature-card"
        @click="handleFeatureClick(item)"
      >
        <img
          :src="getIconPath(item.icon)"
          :alt="item.title"
          class="feature-icon"
        />
        <h2 class="feature-title">{{ item.title }}</h2>
        <p class="feature-description">{{ item.description }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import logoUrl from "@/assets/logo.png";

export default {
  name: "Home",
  data() {
    return {
      logoUrl,
      username: "",
      features: [
        {
          icon: "ipa.png",
          title: "Bảng phiên âm (IPA)",
          description: "Luyện nghe, phát âm chuẩn với 44 âm IPA",
          route: "/ipa",
        },
        {
          icon: "communicate.png",
          title: "Học câu giao tiếp",
          description: "Luyện nghe, nói câu tiếng Anh giao tiếp hằng ngày",
          route: "/conversation",
        },
        {
          icon: "flashcard.png",
          title: "Từ vựng với Flashcard",
          description:
            "Phương pháp học từ vựng nổi tiếng, miễn phí trên Dynonary",
        },
        {
          icon: "favorite.png",
          title: "Từ vựng yêu thích",
          description: "Danh sách từ vựng yêu thích mà bạn đã lưu",
        },
        {
          icon: "verb.png",
          title: "Động từ bất quy tắc",
          description: "Tất cả những động từ bất quy tắc trong tiếng Anh",
          route: "/verb",
        },
        {
          icon: "grammar.png",
          title: "Ngữ pháp",
          description: "Danh sách tổng hợp những cấu trúc câu trong tiếng Anh",
        },
        {
          icon: "grammar.png",
          title: "Listening Test",
          description: "Kiểm tra khả năng nghe của bạn",
          route: "/listening",
        },
        {
          icon: "grammar.png",
          title: "Sentence Test",
          description: "Luyện tập câu tiếng Anh",
          route: "/sentence",
        },
        {
          icon: "grammar.png",
          title: "Đánh giá phát âm",
          description: "Thử tính năng Whisper đánh giá phát âm",
          route: "/Whisper",
        },
      ],
    };
  },
  methods: {
    getIconPath(filename) {
      return new URL(`../assets/icons/${filename}`, import.meta.url).href;
    },
    handleFeatureClick(item) {
      if (item.route) {
        this.$router.push(item.route);
      } else {
        alert(`Tính năng "${item.title}" đang phát triển!`);
      }
    },
    logout() {
      localStorage.removeItem("username");
      this.$router.push("/");
    },
  },
  mounted() {
    // ✅ Kiểm tra username thay vì token
    const user = localStorage.getItem("username");
    if (!user) {
      console.warn("⚠️ Chưa đăng nhập, quay lại trang Login");
      this.$router.push("/");
    } else {
      this.username = user;
      console.log("✅ Đăng nhập với username:", user);
    }
  },
};
</script>

<style scoped>
.app-wrapper {
  background-color: #1a1a2e;
  color: #ffffff;
  min-height: 100vh;
  padding: 40px 20px;
  box-sizing: border-box;
  font-family: "Segoe UI", sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.header-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 48px;
  width: 100%;
}

.title-container {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
  max-width: 1100px;
  margin-bottom: 8px;
}

.logo {
  width: 60px;
  margin-right: 16px;
}

.text-title {
  display: flex;
  align-items: center;
}

.title {
  font-size: 32px;
  font-weight: bold;
  margin: 0;
  color: #ffffff;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
  width: 100%;
  max-width: 1100px;
}

.feature-card {
  background-color: #2a2a3d;
  border-radius: 16px;
  padding: 24px;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.05);
  cursor: pointer;
}

.feature-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 8px 20px rgba(255, 255, 255, 0.1);
}

.feature-icon {
  width: 60px;
  height: 60px;
  margin-bottom: 16px;
}

.feature-title {
  font-size: 18px;
  font-weight: bold;
  color: #ffffff;
  margin: 0;
}

.feature-description {
  font-size: 14px;
  color: #b0b0c3;
  margin-top: 10px;
}
</style>

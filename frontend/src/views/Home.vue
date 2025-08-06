<template>
  <div class="app-wrapper">
    <div class="header-section">
      <div class="title-container">
        <div class="logo-title">
          <img :src="logoUrl" alt="English Tutor" class="logo" />
          <h1 class="title">English Tutor</h1>
        </div>
        <div class="user-section">
          <div class="user-info">
            <img :src="avatarUrl" alt="User Avatar" class="user-avatar" />
            <span class="user-name">{{ username }}</span>
          </div>
          <div class="account-menu-wrapper" @click="toggleMenu">
            <img src="../assets/icons/triangle_down.png" alt="Menu" class="menu-icon" :class="{ rotated: showMenu }" />
            <div v-if="showMenu" class="account-menu">
              <div class="menu-item" @click="goToProfile">Thông tin tài khoản</div>
              <div class="menu-item" @click="logout">Logout</div>
            </div>
          </div>
        </div>
        </div>
    </div>

    <div class="feature-grid">
      <div v-for="item in features" :key="item.title" class="feature-card" @click="handleFeatureClick(item)">
        <img :src="getIconPath(item.icon)" :alt="item.title" class="feature-icon" />
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
      showMenu: false,
      avatarUrl: new URL("../assets/logo.png", import.meta.url).href,
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
          route: "/whisper",
        },
        {
          icon: "dictionary.png",
          title: "Từ điển",
          description: "Tra cứu nghĩa từ tiếng Anh nhanh chóng",
          route: "/dictionary",
        },
        {
          icon: "favorite.png",
          title: "Từ vựng yêu thích",
          description: "Danh sách từ vựng yêu thích mà bạn đã lưu",
          route: "/saved",
        },
        {
          icon: "verb.png",
          title: "Động từ bất quy tắc",
          description: "Tất cả những động từ bất quy tắc trong tiếng Anh",
          route: "/verb",
        },
        {
          icon: "grammaricon.png",
          title: "Ngữ pháp",
          description: "Danh sách tổng hợp những cấu trúc câu trong tiếng Anh",
          route: "/grammar",
        },
        {
          icon: "listeningtest.png",
          title: "Luyện nghe từ vựng",
          description: "Kiểm tra khả năng nghe của bạn với nhiều chủ đề khác nhau",
          route: "/listening",
        },
        {
          icon: "sentencetest.png",
          title: "Học câu tiếng Anh",
          description: "Luyện nghe các câu tiếng Anh",
          route: "/sentence",
        },
        {
          icon: "feedback.png",
          title: "Góp ý & Phản hồi",
          description: "Gửi góp ý, phản hồi để cải thiện ứng dụng",
          route: "/feedback",
        },
      ],
    };
  },
  methods: {
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    getIconPath(filename) {
      return new URL(`../assets/icons/${filename}`, import.meta.url).href;
    },
    handleFeatureClick(item) {
      if (item.route) this.$router.push(item.route);
      else alert(`Tính năng "${item.title}" đang phát triển!`);
    },
    goToProfile() {
      this.$router.push("/profile");
    },
    logout() {
      localStorage.removeItem("username");
      localStorage.removeItem("token"); // ✅ xóa token luôn
      sessionStorage.removeItem("sessionUser");
      this.$router.push("/");
    },
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    checkAuth() {
      const user = sessionStorage.getItem("sessionUser") || localStorage.getItem("username");
      const token = localStorage.getItem("token");

      if (!user || !token) {
        console.warn("⚠️ Token hoặc User không hợp lệ → quay về Login");
        this.logout(); // ✅ gọi logout để clear toàn bộ
      } else {
        this.username = user;
      }
    },
  },
  mounted() {
    const user = localStorage.getItem("username");
    this.checkAuth();
    if (user) {
      this.username = user;
    }
  },
};
</script>

<style scoped>
.app-wrapper {
  background-image: url("../assets/images/background.jpg");
  background-size:100% 100%;
  background-position: center;
  color: #ffffff;
  min-height: 100vh;
  padding: 40px 20px;
  box-sizing: border-box;
  font-family: "Poppins", sans-serif;
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
  justify-content: space-between;
  width: 100%;
  max-width: 1100px;
}

.logo-title {
  display: flex;
  align-items: center;
}

.logo {
  width: 60px;
  margin-right: 16px;
}

.title {
  font-size: 32px;
  font-weight: bold;
  background: linear-gradient(90deg, #222222, #575656, #222222);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}

.user-section {
  display: flex;
  align-items: center;
  position: relative;
}

.user-info {
  display: flex;
  align-items: center;
  background: transparent; /* Bỏ border */
  padding: 0;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 8px;
  box-shadow: 0 0 12px rgba(255, 255, 255, 0.4);
}

.user-name {
  font-size: 16px;
  color: #2a2929;
  margin-right: 12px;
}

.account-menu-wrapper {
  position: relative;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.menu-icon {
  width: 18px;
  height: 18px;
  transition: transform 0.3s ease;
  transform: rotate(-90deg);
}

.menu-icon.rotated {
  transform: rotate(0deg);
}

.account-menu {
  position: absolute;
  right: 0;
  top: 120%;
  background: rgba(30, 30, 45, 0.95);
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
  margin-top: 8px;
  z-index: 999;
  min-width: 160px;
  overflow: hidden;
}

.menu-item {
  padding: 12px 16px;
  color: #ffffff;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.3s, color 0.3s;
}

.menu-item:hover {
  background: rgba(255, 255, 255, 0.929);
  color: rgb(4, 4, 4);
  box-shadow: inset 0 0 5px rgba(254, 254, 254, 0.3);
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 24px;
  width: 100%;
  max-width: 1100px;
}

.feature-card {
  background: rgba(187, 102, 198, 0.245); /* Tối hơn */
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(12px);
  border-radius: 20px;
  padding: 24px;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6);
  cursor: pointer;
}
.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
  background: rgba(255, 255, 255, 0.193); /* Sáng lên nhẹ nhàng */
  border-color: rgba(255, 255, 255, 0.12);
}

.feature-icon {
width: 60px;
height: 60px;
margin-bottom: 16px;
filter: brightness(1.2) contrast(1.1) drop-shadow(0 0 8px rgba(0, 0, 0, 0.6)); /* Giảm độ sáng và tương phản */
}

.feature-title {
  font-size: 18px;
  font-weight: bold;
  color: #2a2929;
  margin: 0;
}

.feature-description {
  font-size: 14px;
  color: #2a2929;
  margin-top: 10px;
}

@media (max-width: 768px) {
  .feature-grid {
    gap: 16px;
  }
}
</style>
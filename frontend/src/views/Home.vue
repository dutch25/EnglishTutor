<template>
  <div class="app-wrapper">
    <div class="header-section">
      <div class="title-container">
        <div class="logo-title">
          <img :src="logoUrl" alt="English Tutor" class="logo" />
          <h1 class="title">English Tutor</h1>
        </div>
        <!-- ✅ Góc phải: User Section (Avatar + Name + Menu) -->
        <div class="user-section">
          <div class="user-info">
            <img :src="avatarUrl" alt="User Avatar" class="user-avatar" />
            <span class="user-name">{{ username }}</span>
          </div>
          <div class="account-menu-wrapper" @click="toggleMenu">
            <img src="../assets/icons/triangle_down.png" alt="Menu" class="menu-icon" :class="{ rotated: showMenu }"/>
            <div v-if="showMenu" class="account-menu">
              <div class="menu-item" @click="goToProfile">Thông tin tài khoản</div>
              <div class="menu-item" @click="logout">Logout</div>
            </div>
          </div>
        </div>
        <!-- END user-section -->
      </div>
    </div>

    <!-- 🔹 Grid Features -->
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
          route: "/saved",
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
        {
          icon: "dictionary.png",
          title: "Từ điển",
          description: "Tra cứu nghĩa từ tiếng Anh nhanh chóng",
          route: "/dictionary",
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
      const user =
        sessionStorage.getItem("sessionUser") ||
        localStorage.getItem("username");
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
  color: #ffffff;
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
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 8px;
}

.user-name {
  font-size: 16px;
  color: #ffffff;
  margin-right: 12px;
}

.user-section {
  display: flex;
  align-items: center;
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
  transform: rotate(-90deg); /* Mặc định nằm ngang */
}

.menu-icon.rotated {
  transform: rotate(0deg); /* Khi mở menu thì quay xuống dưới */
}

.account-menu {
  position: absolute;
  right: 0;
  top: 120%;
  background-color: #2a2a3d;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  margin-top: 8px;
  z-index: 999;
  min-width: 160px;
}

.menu-item {
  padding: 10px 16px;
  color: #ffffff;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.menu-item:hover {
  background-color: #40405a;
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
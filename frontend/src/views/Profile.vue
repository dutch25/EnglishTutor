```html
<template>
  <div class="profile-wrapper">
    <h1 class="profile-title">Thông tin cá nhân</h1>
    <div class="profile-content">
      <div class="info-section">
        <div class="info-item">
          <label>Tên tài khoản:</label>
          <span>{{ username }}</span>
        </div>
        <div class="info-item">
          <label>Email:</label>
          <span>{{ email }}</span>
        </div>
        <div class="info-item">
          <label>Số Điện Thoại:</label>
          <span>{{ phone }}</span>
        </div>
        <div class="info-item-description">
          <label>Mô tả bản thân:</label>
          <span class="description-box">{{ description }}</span>
        </div>
        <div class="info-item">
          <label>Mật khẩu:</label>
          <span>
            <button @click="toggleChangePasswordForm" class="toggle-btn">Thay đổi mật khẩu</button>
          </span>
        </div>
      </div>

      <!-- FORM ĐỔI MẬT KHẨU -->
      <div v-if="showChangePassword" class="password-change-section">
        <div class="form-row">
          <label>Mật khẩu cũ:</label>
          <input :type="showOldPassword ? 'text' : 'password'" v-model="oldPassword" />
        </div>
        <div class="form-row">
          <label>Mật khẩu mới:</label>
          <input :type="showNewPassword ? 'text' : 'password'" v-model="newPassword" />
        </div>
        <div class="form-row">
          <label>Xác nhận mật khẩu:</label>
          <input :type="showConfirmPassword ? 'text' : 'password'" v-model="confirmPassword" />
        </div>
        <div class="button-row">
          <button @click="cancelChangePassword" class="cancel-btn">Hủy bỏ</button>
          <button @click="submitChangePassword" class="save-btn">Lưu thay đổi</button>
        </div>
      </div>

      <div class="button-group">
        <button @click="goHome" class="action-btn">Quay lại Trang chủ</button>
        <button @click="editProfile" class="action-btn">Sửa hồ sơ</button>
      </div>
    </div>

    <!-- 🔥 Toast Notification -->
    <div v-if="toast.show" :class="['toast', toast.type]">
      {{ toast.message }}
    </div>
  </div>
</template>

<script>
export default {
  name: "Profile",
  data() {
    return {
      username: "",
      email: "",
      phone: "",
      description: "",
      oldPassword: "",
      newPassword: "",
      confirmPassword: "",
      showChangePassword: false,
      showOldPassword: false,
      showNewPassword: false,
      showConfirmPassword: false,
      toast: {
        show: false,
        message: "",
        type: "success",
      },
    };
  },
  methods: {
    fetchUserInfo() {
      const user = localStorage.getItem("username");
      if (!user) {
        console.warn("⚠️ Chưa đăng nhập, quay lại trang Login");
        this.$router.push("/");
      } else {
        this.username = user;
        fetch(`http://localhost:8000/api/user/${user}`)
          .then((response) => response.json())
          .then((data) => {
            this.email = data.email || "Chưa có email";
            this.phone = data.phone || "Chưa có số điện thoại";
            this.description = data.description || "Chưa có mô tả";
          })
          .catch((error) => {
            console.error("Lỗi khi lấy thông tin:", error);
          });
      }
    },

    toggleChangePasswordForm() {
      this.showChangePassword = true;
    },
    cancelChangePassword() {
      this.showChangePassword = false;
      this.oldPassword = "";
      this.newPassword = "";
      this.confirmPassword = "";
    },
    submitChangePassword() {
      if (!this.oldPassword || !this.newPassword || !this.confirmPassword) {
        this.showToast("Vui lòng nhập đầy đủ các trường!", "error");
        return;
      }
      if (this.newPassword !== this.confirmPassword) {
        this.showToast("Mật khẩu mới và xác nhận không khớp!", "error");
        return;
      }

      fetch("http://localhost:8000/api/user/change-password", {
        method: "PUT", // Đồng bộ với backend
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: this.username,
          old_password: this.oldPassword,
          new_password: this.newPassword,
        }),
      })
        .then((res) => {
          if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
          }
          return res.json();
        })
        .then((data) => {
          if (data.detail) {
            this.showToast(data.detail, "error");
          } else {
            this.showToast("Đổi mật khẩu thành công! Vui lòng đăng nhập lại.", "success");
            localStorage.removeItem("username");
            setTimeout(() => {
              this.$router.push("/");
            }, 2000);
          }
        })
        .catch((error) => {
          console.error("Lỗi:", error);
          this.showToast(`Lỗi kết nối tới server! (${error.message})`, "error");
        });
    },
    goHome() {
      this.$router.push("/home");
    },
    editProfile() {
      this.$router.push("/edit-profile"); // Tạo 1 trang EditProfile.vue nếu muốn
    },
    showToast(message, type = "success") {
      this.toast.message = message;
      this.toast.type = type;
      this.toast.show = true;
      setTimeout(() => (this.toast.show = false), 3000); // Hiển thị toast trong 3 giây
    },
  },
  mounted() {
    this.fetchUserInfo();
    this.syncUsername = localStorage.getItem("username");
    this.checkUsernameInterval = setInterval(() => {
      const currentUsername = localStorage.getItem("username");
      if (currentUsername !== this.syncUsername) {
        this.syncUsername = currentUsername;
        this.username = currentUsername;
        this.fetchUserInfo(); // Refetch khi username thay đổi
      }
    }, 1000);
  },
  activated() {
    this.fetchUserInfo();
  },
  beforeUnmount() {
    clearInterval(this.checkUsernameInterval);
  },
};
</script>

<style scoped>
.profile-wrapper {
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

.profile-title {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 24px;
}

.profile-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #2a2a3d;
  padding: 24px;
  border-radius: 16px;
  width: 100%;
  max-width: 500px;
}

.info-section {
  width: 100%;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 21px;
}

.info-item-description {
  display: flex;
  align-items: flex-start;
  margin-bottom: 21px;
}

.info-item-description label {
  width: 150px;
  font-weight: bold;
}

.info-item label {
  width: 150px;
  font-weight: bold;
}

.info-item span {
  flex: 1;
  text-align: left;
}

.toggle-btn {
  background-color: #3b3b50;
  color: #ffffff;
  border: none;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
}
.toggle-btn:hover {
  background-color: #50506e;
}

.description-box {
  flex: 1;
  padding: 10px;
  background-color: #2a2a3d;
  color: #ffffff;
  border: 1px solid #ffffff;
  border-radius: 6px;
  min-height: 100px; /* Gấp 3 lần các dòng thông tin khác */
  box-sizing: border-box;
}

/* FORM ĐỔI MẬT KHẨU */
.password-change-section {
  margin-top: 20px;
  padding: 16px;
  background-color: #1e1e2e;
  border-radius: 10px;
  width: 100%;
}

.form-row {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
}

.form-row label {
  width: 150px;
  font-weight: bold;
}

.form-row input {
  flex: 1;
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  background-color: #2a2a3d;
  color: #fff;
}

/* Nút Hủy & Lưu */
.button-row {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.cancel-btn,
.save-btn {
  padding: 6px 14px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

.cancel-btn {
  background-color: #6c6c6c;
  color: white;
}

.save-btn {
  background-color: #3b82f6;
  color: white;
}

/* Nút Quay lại & Sửa hồ sơ */
.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
  width: 100%;
}

.action-btn {
  background-color: #3b3b50;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  width: 48%;
}

.action-btn:hover {
  background-color: #50506e;
}

/* 🔹 Toast Notification */
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  background: #333;
  color: #fff;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.3s ease;
}

.toast.success {
  background: #4caf50;
}

.toast.error {
  background: #e53935;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: none;
  }
}
</style>
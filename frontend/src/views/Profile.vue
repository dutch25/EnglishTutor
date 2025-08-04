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

      <transition name="fade">
        <div v-if="showChangePassword" class="password-change-section">
          <div class="form-row">
            <label>Mật khẩu cũ:</label>
            <div class="password-input">
              <input :type="showOldPassword ? 'text' : 'password'" v-model="oldPassword" />
              <i :class="showOldPassword ? 'fas fa-eye-slash' : 'fas fa-eye'" class="toggle-eye" @click="showOldPassword = !showOldPassword"></i>
            </div>
          </div>
          <div class="form-row">
            <label>Mật khẩu mới:</label>
            <div class="password-input">
              <input :type="showNewPassword ? 'text' : 'password'" v-model="newPassword" />
              <i :class="showNewPassword ? 'fas fa-eye-slash' : 'fas fa-eye'" class="toggle-eye" @click="showNewPassword = !showNewPassword"></i>
            </div>
          </div>
          <div class="form-row">
            <label>Xác nhận mật khẩu:</label>
            <div class="password-input">
              <input :type="showConfirmPassword ? 'text' : 'password'" v-model="confirmPassword" />
              <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'" class="toggle-eye" @click="showConfirmPassword = !showConfirmPassword"></i>
            </div>
          </div>
          <div class="button-row">
            <button @click="cancelChangePassword" class="cancel-btn">Hủy</button>
            <button @click="submitChangePassword" class="save-btn">Lưu</button>
          </div>
        </div>
      </transition>

      <div class="button-group">
        <button @click="goHome" class="action-btn">🏠 Trang chủ</button>
        <button @click="editProfile" class="action-btn edit-btn">✏️ Sửa hồ sơ</button>
      </div>
    </div>

    <transition name="slide-fade">
      <div v-if="toast.show" :class="['toast', toast.type]">
        {{ toast.message }}
      </div>
    </transition>
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
            localStorage.removeItem("token");
            localStorage.removeItem("username");
            setTimeout(() => {
              this.$router.push("/");
            }, 1500);
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
/* Background Gradient */
.profile-wrapper {
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  color: #ffffff;
  min-height: 100vh;
  padding: 40px 20px;
  font-family: 'Poppins', sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-title {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 30px;
  background: linear-gradient(90deg, #00c6ff, #0072ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.profile-content {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  padding: 30px;
  border-radius: 20px;
  width: 100%;
  max-width: 500px;
}

.info-section {
  width: 100%;
}

.info-item, .info-item-description {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
}

.info-item label, .info-item-description label {
  width: 140px;
  font-weight: 600;
}

.info-item span {
  flex: 1;
  word-break: break-word;
}

.description-box {
  flex: 1;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  padding: 12px;
  min-height: 100px;
}

/* Buttons */
.toggle-btn {
  background: linear-gradient(135deg, #ff416c, #ff4b2b);
  color: #fff;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}
.toggle-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 65, 108, 0.4);
}

/* Change Password Form */
.password-change-section {
  margin-top: 25px;
  padding: 20px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 16px;
}

.password-input {
  position: relative;
  flex: 1;
  display: flex;
  align-items: center;
}

.password-input input {
  width: 100%;
  padding-right: 40px; /* Chừa chỗ cho icon */
  padding-left: 10px;
  height: 38px;
  line-height: 38px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
  box-sizing: border-box;
}

.toggle-eye {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: #ccc;
  font-size: 18px;
  transition: all 0.2s ease;
}

.toggle-eye:hover {
  color: #00c6ff;
  transform: translateY(-50%) scale(1.2);
}

.form-row {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.form-row label {
  width: 140px;
  font-weight: 600;
  flex-shrink: 0;
}

.form-row input {
  flex: 1;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}

/* Action Buttons */
.button-row {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 10px;
}

.cancel-btn, .save-btn {
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-weight: 600;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
}
.save-btn {
  background: linear-gradient(135deg, #00c6ff, #0072ff);
  color: white;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.action-btn {
  width: 48%;
  padding: 12px 0;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  background: linear-gradient(135deg, #12c2e9, #c471ed);
  color: white;
  border: none;
  transition: all 0.3s ease;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(196, 113, 237, 0.4);
}

.edit-btn {
  background: linear-gradient(135deg, #f7971e, #ffd200);
}

/* Toast Notification */
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 14px 24px;
  border-radius: 12px;
  font-weight: 600;
  color: #fff;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
}

.toast.success {
  background: linear-gradient(135deg, #00c853, #b2ff59);
}

.toast.error {
  background: linear-gradient(135deg, #d50000, #ff8a80);
}

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active {
  transition: all 0.5s ease;
}
.slide-fade-enter, .slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
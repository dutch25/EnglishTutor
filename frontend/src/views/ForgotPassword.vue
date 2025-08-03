<template>
  <div class="forgot-password-wrapper">
    <div class="forgot-card">
      <h2>Quên mật khẩu</h2>
      <div class="form-group">
        <label>Số điện thoại:</label>
        <input v-model="phone" type="text" />
      </div>
      <button class="send-otp-btn" @click="sendOTP">Gửi mã xác nhận</button>

      <div v-if="otpSent" class="otp-section">
        <div class="form-group">
          <label>Nhập mã OTP:</label>
          <input v-model="otpCode" type="text" />
        </div>
        <div class="form-group">
          <label>Mật khẩu mới:</label>
          <input v-model="newPassword" type="password" />
        </div>
        <button class="verify-otp-btn" @click="verifyAndResetPassword">Xác nhận & Đổi mật khẩu</button>
      </div>

      <div v-if="message" class="message">{{ message }}</div>
      <button @click="backLogin" class="send-otp-btn">Quay lại</button>
    </div>

    <!-- 🔥 Toast Notification -->
    <div v-if="toast.show" :class="['toast', toast.type]">
      {{ toast.message }}
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      phone: "",
      otpCode: "",
      newPassword: "",
      otpSent: false,
      message: "",
      toast: {
        show: false,
        message: "",
        type: "success",
      },
    };
  },
  methods: {
    async sendOTP() {
      try {
        const res = await fetch("http://localhost:8000/api/user/send-otp", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ phone: this.phone }),
        });
        const data = await res.json();
        if (data.detail) {
          this.showToast(data.detail, "error");
        } else {
          this.showToast("Mã xác nhận đã được gửi!", "success");
          this.otpSent = true;
        }
      } catch (err) {
        console.error("❌ [DEBUG] Lỗi gửi OTP:", err);
        this.showToast("Lỗi kết nối tới server!", "error");
      }
    },
    async verifyAndResetPassword() {
      try {
        const res = await fetch("http://localhost:8000/api/user/reset-password", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            phone: this.phone,
            otp_code: this.otpCode,
            new_password: this.newPassword,
          }),
        });
        const data = await res.json();
        if (data.detail) {
          this.showToast(data.detail, "error");
        } else {
          this.showToast("Mật khẩu đã được đặt lại thành công!", "success");
          setTimeout(() => {
            this.$router.push("/");
          }, 2000);
        }
      } catch (err) {
        console.error("❌ [DEBUG] Lỗi reset mật khẩu:", err);
        this.showToast("Lỗi kết nối tới server!", "error");
      }
    },
    backLogin() {
      this.$router.push("/");
    },
    showToast(message, type = "success") {
      this.toast.message = message;
      this.toast.type = type;
      this.toast.show = true;
      setTimeout(() => (this.toast.show = false), 3000); // Hiển thị toast trong 3 giây
    },
  },
};
</script>

<style scoped>
.forgot-password-wrapper {
  background-color: #1a1a2e;
  color: #ffffff;
  min-height: 100vh;
  padding: 40px 20px;
  font-family: "Segoe UI", sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
}

.forgot-card {
  background-color: #2a2a3d;
  padding: 32px;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  width: 100%;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 1px solid #3b3b50;
}

.forgot-card h2 {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 24px;
}

.form-group {
  width: 100%;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 6px;
}

.form-group input {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #4f4f70;
  background-color: #1f1f2e;
  color: #fff;
  font-size: 16px;
}

.send-otp-btn, .verify-otp-btn {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 10px;
  cursor: pointer;
  margin-top: 10px;
  border: none;
  transition: background-color 0.3s;
}

.send-otp-btn {
  background-color: #3b82f6;
}

.send-otp-btn:hover {
  background-color: #2563eb;
}

.verify-otp-btn {
  background-color: #10b981;
}

.verify-otp-btn:hover {
  background-color: #059669;
}

.message {
  margin-top: 20px;
  font-size: 15px;
  color: #52c41a;
  text-align: center;
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
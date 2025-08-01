<template>
  <div>
    <!-- Header -->
    <div class="top-header">
      <div class="logo-title">
        <img src="@/assets/logo.png" alt="Logo EngAI" class="header-logo" />
        <span class="title-text">Dynonary English</span>
      </div>
    </div>

    <!-- Login Form -->
    <div class="auth-wrapper">
      <div class="auth-box">
        <h2>Đăng Nhập</h2>
        <form @submit.prevent="login">
          <input
            v-model="username"
            type="text"
            placeholder="Email hoặc Tên đăng nhập"
            required
          />

          <div class="password-wrapper">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="Mật khẩu"
              required
            />
            <span class="toggle-password" @click="showPassword = !showPassword">
              {{ showPassword ? "Ẩn" : "Hiện" }}
            </span>
          </div>

          <button type="submit">Đăng nhập</button>
        </form>

        <p class="switch-link">
          Chưa có tài khoản?
          <router-link to="/register">Đăng ký ngay</router-link>
        </p>
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
  data() {
    return {
      username: "",
      password: "",
      showPassword: false,
      toast: {
        show: false,
        message: "",
        type: "success",
      },
    };
  },
  methods: {
    async login() {
      console.clear();
      console.log("🔹 [DEBUG] Bắt đầu login...");

      // Kiểm tra độ dài email (tối thiểu 5 ký tự)
      if (this.username.length < 5) {
        this.showToast("Email phải có ít nhất 5 ký tự!", "error");
        return;
      }

      // Kiểm tra độ dài mật khẩu (tối thiểu 8 ký tự)
      if (this.password.length < 8) {
        this.showToast("Mật khẩu phải có ít nhất 8 ký tự!", "error");
        return;
      }

      try {
        const res = await fetch("http://localhost:8000/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            login_input: this.username,
            password: this.password,
          }),
        });

        const data = await res.json();
        console.log("🔹 [DEBUG] Response từ server:", data);

        if (!res.ok) {
          // ✅ Parse lỗi trả về từ FastAPI
          let msg = "Sai tài khoản hoặc mật khẩu!";
          if (Array.isArray(data) && data[0]?.msg) {
            msg = data[0].msg;
          } else if (data?.detail) {
            msg = data.detail;
          } else if (data?.msg) {
            msg = data.msg;
          }

          this.showToast(msg, "error");
          return;
        }

        if (data.username) {
          localStorage.setItem("username", data.username);
        }

        this.showToast("✅ Đăng nhập thành công!", "success");

        setTimeout(() => {
          this.$router.push("/home");
        }, 1000);
      } catch (err) {
        console.error("❌ [DEBUG] Lỗi kết nối:", err);
        this.showToast("Lỗi kết nối tới server!", "error");
      }
    },

    showToast(message, type = "success") {
      this.toast.message = message;
      this.toast.type = type;
      this.toast.show = true;
      setTimeout(() => (this.toast.show = false), 3000);
    },
  },
};
</script>

<style scoped>
/* Header */
.top-header {
  background-color: #62676b;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}
.logo-title {
  display: flex;
  align-items: center;
}
.header-logo {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  margin-right: 12px;
}
.title-text {
  font-size: 22px;
  font-weight: 700;
  color: #ffffff;
}

/* Form */
.auth-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #62676b, #707275);
  height: calc(100vh - 72px);
}
.auth-box {
  background: #e6e6e6;
  padding: 36px;
  border-radius: 16px;
  width: 360px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}
.auth-box h2 {
  text-align: center;
  color: #3c80d1;
  margin-bottom: 24px;
}
input {
  width: 100%;
  padding: 12px 16px;
  margin: 12px 0;
  border: 1px solid #ccd5db;
  border-radius: 12px;
}
.password-wrapper {
  position: relative;
}
.toggle-password {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  color: #007acc;
}
button {
  width: 100%;
  padding: 12px;
  background: #4f9ec4;
  color: #fff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}
button:hover {
  background: #3b8ab0;
}
.switch-link {
  text-align: center;
  margin-top: 16px;
}

/* ✅ Toast */
.toast {
  position: fixed;
  top: 20px; /* Giữ ở góc phải trên cùng */
  right: 20px; /* Giữ ở góc phải trên cùng */
  background: #333;
  color: #fff;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.3s ease;
}
.toast.success {
  background: #4caf50; /* Khôi phục màu xanh lá cho "Đăng nhập thành công" */
}
.toast.error {
  background: #e53935; /* Giữ màu đỏ cho lỗi */
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

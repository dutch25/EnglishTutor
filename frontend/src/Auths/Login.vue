
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

          <div class="password-field">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="Mật khẩu"
              required
            />
            <span class="toggle-password" @click="togglePassword">
              <i :class="['fas', showPassword ? 'fa-eye-slash' : 'fa-eye']"></i>
            </span>
          </div>
          <a class="forgot-password-link" @click="goToForgotPassword">Quên mật khẩu?</a>
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
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    async login() {
      console.log("🔹 [DEBUG] Bắt đầu login...");
      
      // ✅ Validate input
      if (this.username.length < 5) {
        this.showToast("Email phải có ít nhất 5 ký tự!", "error");
        return;
      }
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
          let msg = "";
          if (res.status === 422) {
            msg = data?.detail || data?.msg || "Dữ liệu không hợp lệ, vui lòng kiểm tra lại!";
          } else {
            msg = data?.detail || data?.msg || "Sai tài khoản hoặc mật khẩu!";
          }
          this.showToast(msg, "error");
          return;
        }

        // ✅ Lưu session, username và token
        if (data.username) {
          localStorage.setItem("username", data.username);
          localStorage.setItem("email", data.email); // Lưu email từ API
          localStorage.setItem("password", data.password); // Lưu mật khẩu (nếu cần)
          sessionStorage.setItem("sessionUser", data.username);
          localStorage.setItem("token", data.token || "dummy-token");
        }

        // ✅ Hiển thị thông báo thành công
        this.showToast("✅ Đăng nhập thành công!", "success");

        // ✅ Chuyển sang Home sau 1s
        setTimeout(() => {
          this.$router.push("/home");
        }, 1000);
      } catch (err) {
        console.error("❌ [DEBUG] Lỗi kết nối:", err);
        this.showToast("Lỗi kết nối tới server!", "error");
      }
    },

    goToForgotPassword() {
      this.$router.push("/forgot-password");
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
/* 🔹 Header */
.top-header {
  background: linear-gradient(135deg, #606468, #6A6D71);
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
}
.title-text {
  font-size: 22px;
  font-weight: 700;
  color: #ffffff;
}

/* 🔹 Form */
.auth-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #62676b, #707275);
  height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.auth-box {
  background-color: #e6e6e6;
  padding: 36px;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  width: 360px;
  animation: fadeIn 0.5s ease;
}

.auth-box h2 {
  text-align: center;
  color: #3c80d1;
  margin-bottom: 24px;
  font-weight: 600;
}

input {
  width: 100%;
  padding: 12px 16px;
  margin: 12px 0;
  border: 1px solid #ccd5db;
  border-radius: 12px;
  font-size: 15.5px;
  background-color: #fff;
  box-sizing: border-box;
  transition: border-color 0.2s, box-shadow 0.2s;
}

input:focus {
  border-color: #4f9ec4;
  outline: none;
  box-shadow: 0 0 0 2px rgba(79, 158, 196, 0.15);
}

.password-field {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  font-size: 16px;
  user-select: none;
  color: #007acc; /* Màu icon tương tự màu chữ "Quên mật khẩu?" */
}

.toggle-password:hover {
  color: #3b8ab0; /* Hiệu ứng hover giống nút */
}

.forgot-password-link {
  display: block;
  text-decoration: underline;
  color: #007acc;
  cursor: pointer;
  margin: 6px 0 6px 0;
  text-align: right;
  padding-right: 20px;
  font-size: 14px;
}

button {
  width: 100%;
  padding: 12px;
  background-color: #4f9ec4;
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 6px;
}

button:hover {
  background-color: #3b8ab0;
}

.switch-link {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: #666;
}

.switch-link a {
  color: #4f9ec4;
  text-decoration: none;
  font-weight: 500;
}

.switch-link a:hover {
  text-decoration: underline;
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
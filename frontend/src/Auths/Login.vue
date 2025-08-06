<template>
  <div class="login-page">
    <div :class="['left-panel', { 'slide-in-left': true, 'slide-in-active': animate }]">
      <div class="welcome-text">
        <div class="logo-title">
          <img src="@/assets/logo.png" alt="Logo EngAI" class="header-logo" />
          <span class="title-text">EngAI</span>
        </div>
        <h1>Welcome!</h1>
        <p>Chúng tôi có thể giúp bạn học tiếng Anh một cách hiệu quả.<br/>
          Cải thiện kỹ năng ngôn ngữ của bạn với chúng tôi. <br/>
          Học tiếng Anh không khó, đã có EngAI</p>
        <a href="https://github.com/dutch25/EnglishTutor" target="_blank" class="learn-more-btn">Learn More</a>
      </div>
    </div>

    <div :class="['right-panel', { 'slide-in-right': true, 'slide-in-active': animate }]">
      <form @submit.prevent="login">
        <h2>Sign in</h2>

        <div class="input-group email-field">
          <label>Email hoặc Tên đăng nhập</label>
          <input v-model="username" type="text" placeholder="Nhập email hoặc username" required />
        </div>

        <div class="input-group password-field">
          <label>Mật khẩu</label>
          <input :type="showPassword ? 'text' : 'password'" v-model="password" placeholder="Nhập mật khẩu" required />
          <span class="toggle-password" @click="togglePassword">
            <i :class="['fas', showPassword ? 'fa-eye-slash' : 'fa-eye']"></i>
          </span>
        </div>

        <a class="forgot-password-link" @click="goToForgotPassword">Quên mật khẩu?</a>

        <button type="submit" class="submit-btn">Đăng nhập</button>

        <div class="social-icons">
          <i class="fab fa-facebook-f"></i>
          <i class="fab fa-instagram"></i>
          <i class="fab fa-pinterest-p"></i>
        </div>

        <p class="switch-link">
          Chưa có tài khoản?
          <router-link to="/register">Đăng ký ngay</router-link>
        </p>
      </form>
    </div>

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
      animate: false,
    };
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    async login() {
      console.log("🔹 [DEBUG] Bắt đầu login...");
      
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

        // Lưu thông tin người dùng
        if (data.username) {
          localStorage.setItem("username", data.username);
          localStorage.setItem("email", data.email);
          localStorage.setItem("password", data.password);
          sessionStorage.setItem("sessionUser", data.username);
          localStorage.setItem("token", data.token || "dummy-token");
          localStorage.setItem("user_id", data.id); 
        }
        // Hiển thị thông báo thành công
        this.showToast("✅ Đăng nhập thành công!", "success");

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
      setTimeout(() => (this.toast.show = false), 3000);
    },
  },
  mounted() {
    setTimeout(() => {
      this.animate = true;
    }, 30);
  },
};
</script>

<style scoped>
.login-page {
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #43104e, #200125);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: white;
}

.left-panel {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
  background: rgba(255, 255, 255, 0.03);
}

.welcome-text {
  max-width: 400px;
}

.logo-title {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 40px;
  transform: translateX(-21px);
}

.header-logo {
  width: 100px;
  height: 100px;
  object-fit: contain; 
}

.title-text {
  font-size: 80px;
  font-weight: bold;
}

.welcome-text h1 {
  font-size: 42px;
  margin-bottom: 20px;
}

.welcome-text p {
  font-size: 14px;
  color: #ccc;
  margin-bottom: 20px;
}

.learn-more-btn {
  background: linear-gradient(45deg, #fc466b, #3f5efb);
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 30px;
  cursor: pointer;
  font-size: 14px;
}

.right-panel {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

form {
  background: rgba(255, 255, 255, 0.05);
  padding: 40px 30px;
  border-radius: 12px;
  width: 360px;
  backdrop-filter: blur(10px);
  display: flex;
  flex-direction: column;
  align-items: center;
}

form h2 {
  text-align: center;
  font-size: 28px;
  margin-bottom: 30px;
  width: 100%;
}

.input-group {
  position: relative;
  width: 100%;
  margin-bottom: 20px;
}

label {
  font-size: 12px;
  display: block;
  margin-bottom: 6px;
  color: #ddd;
}

input {
  width: 100%;
  padding: 10px 40px 10px 16px; 
  background: rgba(255, 255, 255, 0.08);
  border: none;
  border-radius: 20px;
  font-size: 14px;
  color: #fff;
  outline: none;
  height: 42px;
  box-sizing: border-box;
}

input::placeholder {
  color: #ccc;
}

input:focus {
  background: rgba(255, 255, 255, 0.15);
}

.password-field .toggle-password {
  position: absolute;
  right: 14px;
  margin-top: 19px;
  transform: translateY(-50%);
  cursor: pointer;
  font-size: 18px;
  color: #000;
  line-height: 1;
}

.forgot-password-link {
  display: block;
  width: 100%;
  text-align: right;
  font-size: 12px;
  margin-bottom: 20px;
  color: #4f9ec4;
  cursor: pointer;
  text-decoration: underline;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(45deg, #fc466b, #3f5efb);
  border: none;
  border-radius: 30px;
  font-size: 14px;
  cursor: pointer;
  margin-bottom: 20px;
}

.social-icons {
  display: flex;
  justify-content: center;
  gap: 20px;
  font-size: 18px;
  color: #fff;
  margin-bottom: 20px;
}

.switch-link {
  text-align: center;
  font-size: 12px;
  color: #ccc;
}

.switch-link a {
  color: #4f9ec4;
  text-decoration: none;
}

.switch-link a:hover {
  text-decoration: underline;
}

/* Toast */
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 15px;
  color: white;
  animation: fadeIn 0.3s ease;
}

.toast.success {
  background: #4caf50;
}

.toast.error {
  background: #e53935;
}
.slide-in-left {
  opacity: 0;
  transform: translateX(-50px);
  transition: all 0.8s ease-out;
}

.slide-in-right {
  opacity: 0;
  transform: translateX(50px);
  transition: all 0.8s ease-out;
} 

.slide-in-active {
  opacity: 1 !important;
  transform: translateX(0) !important;
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

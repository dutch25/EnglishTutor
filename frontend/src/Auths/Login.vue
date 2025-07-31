<template>
  <div>
    <!-- Header -->
    <div class="top-header">
      <div class="logo-title">
        <img src="@/assets/logo.png" alt="Logo EngAI" class="header-logo" />
        <span class="title-text">Dynonary English</span>
      </div>
    </div>

    <!-- Login Form Wrapper -->
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
          <div v-if="errors.username" class="error">{{ errors.username }}</div>

          <div class="password-wrapper">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              placeholder="Mật khẩu"
              required
            />
            <span class="toggle-password" @click="showPassword = !showPassword">
              {{ showPassword ? 'Ẩn' : 'Hiện' }}
            </span>
          </div>
          <div v-if="errors.password" class="error">{{ errors.password }}</div>

          <button type="submit">Đăng nhập</button>
        </form>
        <p class="switch-link">
          Chưa có tài khoản?
          <router-link to="/register">Đăng ký ngay</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      password: '',
      showPassword: false,
      errors: {
        username: '',
        email: '',
        password: ''
      }
    };
  },
  methods: {
    async login() {
      this.errors = {}; // Reset lỗi trước đó
      try {
        const res = await fetch('http://localhost:8000/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            login_input: this.username,
            password: this.password
          })
        });

        if (!res.ok) {
          const data = await res.json();
          const message = data.detail;

          // Phân tích lỗi trả về từ backend
          if (message.includes("username")) {
            this.errors.username = "Tên đăng nhập không đúng.";
          } else if (message.includes("password")) {
            this.errors.password = "Mật khẩu không đúng.";
          } else {
            this.errors.username = message;
          }

        } else {
          alert("Đăng nhập thành công!");
          this.$router.push("/home");
        }

      } catch (err) {
        this.errors.username = "Lỗi kết nối. Vui lòng thử lại.";
      }
    }
  }
};
</script>

<style scoped>
/* Header styles */
.top-header {
  background-color: #62676b;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: start;
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

/* Login box styles */
.auth-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #62676b, #707275);
  height: calc(100vh - 72px);
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
  margin: 12px 0 4px 0;
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

.password-wrapper {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  font-size: 18px;
  user-select: none;
}

.error {
  color: red;
  font-size: 13px;
  margin-bottom: 8px;
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
  margin-top: 12px;
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
</style>

<template>
  <div class="auth-wrapper">
    <div class="logo-container">
      <img src="@/assets/logo.png" alt="Logo EngAI" class="logo" />
    </div>
    <div class="auth-box">
      <h2>Đăng Ký</h2>
      <form @submit.prevent="register">
        <input v-model="username" type="text" placeholder="Tên đăng nhập" required />
        <div v-if="errors.username" class="error">{{ errors.username }}</div>

        <input v-model="email" type="text" placeholder="Email" required />
        <div v-if="errors.email" class="error">{{ errors.email }}</div>

        <div class="password-field">
          <input :type="showPassword ? 'text' : 'password'" v-model="password" placeholder="Mật khẩu" required />
          <span @click="togglePassword" class="toggle-eye">{{ showPassword ? 'Ẩn' : 'Hiện' }}</span>
        </div>
        <div v-if="errors.password" class="error">{{ errors.password }}</div>

        <div class="password-field">
          <input :type="showConfirm ? 'text' : 'password'" v-model="confirmPassword" placeholder="Xác nhận mật khẩu" required />
          <span @click="toggleConfirm" class="toggle-eye">{{ showConfirm ? 'Ẩn' : 'Hiện' }}</span>
        </div>
        <div v-if="password && confirmPassword && password !== confirmPassword" class="error">
          Mật khẩu không khớp!
        </div>

        <button type="submit">Đăng ký</button>
      </form>
      <p class="switch-link">
        Đã có tài khoản?
        <router-link to="/">Đăng nhập</router-link>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      showPassword: false,
      showConfirm: false,
      errors: {}
    };
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    toggleConfirm() {
      this.showConfirm = !this.showConfirm;
    },
    validatePasswordStrength(password) {
      const regex = /^(?=.*[A-Z])(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]).{8,}$/;
      return regex.test(password);
    },
    async register() {
      this.errors = {}; // Clear previous errors

      if (!this.validatePasswordStrength(this.password)) {
        this.errors.password = "Mật khẩu phải có ít nhất 8 ký tự, 1 chữ in hoa và 1 ký tự đặc biệt.";
        return;
      }

      if (this.password !== this.confirmPassword) {
        this.errors.confirmPassword = "Mật khẩu không khớp";
        return;
      }

      try {
        const res = await fetch('http://localhost:8000/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password,
            confirm_password: this.confirmPassword
          })
        });

        const data = await res.json();

        if (!res.ok) {
          const detail = data.detail || "";

          if (detail.includes("User already exists") || detail.includes("Tên đăng nhập đã tồn tại")) {
            this.errors.username = "Tên đăng nhập đã tồn tại";
          } else if (res.status === 401 && data.detail.includes("chưa được xác nhận")) {
            this.errors.username = "Tài khoản chưa được xác nhận, vui lòng kiểm tra email.";
          } else if (detail.includes("Email đã được sử dụng")) {
            this.errors.email = "Email đã được sử dụng";
          } else if (detail.includes("Email không hợp lệ")) {
            this.errors.email = "Email không hợp lệ.";
          } else if (detail.includes("Email không tồn tại")) {
            this.errors.email = "Email không tồn tại.";
          } else if (detail.includes("Passwords do not match")) {
            this.errors.confirmPassword = "Mật khẩu không khớp";
          } else {
            this.errors.general = detail;  
          }
        } else {
          alert("Đăng ký thành công!");
          this.$router.push("/");
        }
      } catch (err) {
        console.error(err);
        this.errors.general = "Đã xảy ra lỗi, vui lòng thử lại sau.";
      }
    }
  }
};
</script>

<style scoped>
.error {
  color: red;
  font-size: 0.9em;
}

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

.logo-container {
  margin-bottom: 20px;
  text-align: center;
}

.logo-container img {
  width: 60px;
  height: 60px;
  border-radius: 12px;
}

.logo {
  width: 60px;
  margin-right: 16px;
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

.toggle-eye {
  position: absolute;
  right: 14px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  font-size: 16px;
  user-select: none;
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

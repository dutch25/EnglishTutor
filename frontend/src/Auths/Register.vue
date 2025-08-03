<template>
  <div>
    <div class="top-header">
      <div class="logo-title">
        <img src="@/assets/logo.png" alt="Logo EngAI" class="header-logo" />
        <span class="title-text">Dynonary English</span>
      </div>
    </div>
    <div class="auth-wrapper">
      <div class="auth-box">
        <h2>Đăng Ký</h2>
        <form @submit.prevent="register">
          <input v-model="username" type="text" placeholder="Tên đăng nhập" required />
          <div v-if="errors.username" class="error">{{ errors.username }}</div>

          <input v-model="email" type="text" placeholder="Email" required />
          <div v-if="errors.email" class="error">{{ errors.email }}</div>

          <input v-model="phone" type="text" placeholder="Số điện thoại" required />
          <div v-if="errors.phone" class="error">{{ errors.phone }}</div>

          <div class="password-field">
            <input :type="showPassword ? 'text' : 'password'" v-model="password" placeholder="Mật khẩu" required />
            <span class="toggle-eye" @click="togglePassword">
              <i :class="['fas', showPassword ? 'fa-eye-slash' : 'fa-eye']"></i>
            </span>
          </div>
          <div v-if="errors.password" class="error">{{ errors.password }}</div>

          <div class="password-field">
            <input :type="showConfirm ? 'text' : 'password'" v-model="confirmPassword" placeholder="Xác nhận mật khẩu" required />
            <span class="toggle-eye" @click="toggleConfirm">
              <i :class="['fas', showConfirm ? 'fa-eye-slash' : 'fa-eye']"></i>
            </span>
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
      username: '',
      email: '',
      phone: '',
      password: '',
      confirmPassword: '',
      showPassword: false,
      showConfirm: false,
      errors: {},
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
    toggleConfirm() {
      this.showConfirm = !this.showConfirm;
    },
    validatePasswordStrength(password) {
      const regex = /^(?=.*[A-Z])(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]).{8,}$/;
      return regex.test(password);
    },
    validatePhoneNumber(phone) {
      const phoneRegex = /^(0[3|5|7|8|9])+([0-9]{8})$/;
      return phoneRegex.test(phone);
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

      if (!this.validatePhoneNumber(this.phone)) {
        this.errors.phone = "Số điện thoại không hợp lệ.";
        return;
      }

      console.log("Phone nhập vào:", this.phone);
      if (!this.phone) {
        this.errors.phone = "Vui lòng nhập số điện thoại.";
        return;
      }

      try {
        const res = await fetch('http://localhost:8000/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            phone: this.phone,
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
          } else if (detail.includes("Số điện thoại không hợp lệ")) {
            this.errors.phone = "Số điện thoại không hợp lệ.";
          } else if (detail.includes("Mật khẩu phải có ít nhất 8 ký tự, 1 chữ in hoa và 1 ký tự đặc biệt")) {
            this.errors.password = "Mật khẩu phải có ít nhất 8 ký tự, 1 chữ in hoa và 1 ký tự đặc biệt.";
          } else if (detail.includes("Mật khẩu không khớp")) {
            this.errors.confirmPassword = "Mật khẩu không khớp";
          } else {
            this.errors.general = detail;  
          }
        } else {
          this.showToast("✅ Đăng ký thành công!", "success");
          setTimeout(() => {
            this.$router.push("/");
          }, 1000);
        }
      } catch (err) {
        console.error(err);
        this.errors.general = "Đã xảy ra lỗi, vui lòng thử lại sau.";
      }
    },
    showToast(message, type = "success") {
      this.toast.message = message;
      this.toast.type = type;
      this.toast.show = true;
      setTimeout(() => (this.toast.show = false), 3000);
    },
  }
};
</script>

<style scoped>
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
  color: #007acc; /* Màu icon tương tự màu chữ "Đã có tài khoản?" */
}

.toggle-eye:hover {
  color: #3b8ab0; /* Hiệu ứng hover giống nút */
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
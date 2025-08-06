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
        <button class="learn-more-btn">Learn More</button>
      </div>
    </div>

    <div :class="['right-panel', { 'slide-in-right': true, 'slide-in-active': animate }]">
      <form @submit.prevent="register">
        <h2>Sign Up</h2>

        <div class="input-group">
          <label>Tên đăng nhập</label>
          <input v-model="username" type="text" placeholder="Tên đăng nhập" required />
          <div v-if="errors.username" class="error">{{ errors.username }}</div>
        </div>

        <div class="input-group">
          <label>Email</label>
          <input v-model="email" type="text" placeholder="Email" required />
          <div v-if="errors.email" class="error">{{ errors.email }}</div>
        </div>

        <div class="input-group">
          <label>Số điện thoại</label>
          <input v-model="phone" type="text" placeholder="Số điện thoại" required />
          <div v-if="errors.phone" class="error">{{ errors.phone }}</div>
        </div>

        <div class="input-group password-field">
          <label>Mật khẩu</label>
          <input :type="showPassword ? 'text' : 'password'" v-model="password" placeholder="Mật khẩu" required />
          <span class="toggle-password" @click="togglePassword">
            <i :class="['fas', showPassword ? 'fa-eye-slash' : 'fa-eye']"></i>
          </span>
          <div v-if="errors.password" class="error">{{ errors.password }}</div>
        </div>

        <div class="input-group password-field">
          <label>Xác nhận mật khẩu</label>
          <input :type="showConfirm ? 'text' : 'password'" v-model="confirmPassword" placeholder="Xác nhận mật khẩu" required />
          <span class="toggle-password" @click="toggleConfirm">
            <i :class="['fas', showConfirm ? 'fa-eye-slash' : 'fa-eye']"></i>
          </span>
          <div v-if="password && confirmPassword && password !== confirmPassword" class="error">Mật khẩu không khớp!</div>
        </div>

        <button type="submit" class="submit-btn">Đăng ký</button>

        <p class="switch-link">
          Đã có tài khoản?
          <router-link to="/">Đăng nhập</router-link>
        </p>
      </form>
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
      animate: false,
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
  },
  mounted() {
    // Delay 100ms to trigger CSS transition smoothly
    setTimeout(() => {
      this.animate = true;
    }, 30);
  },
};
</script>

<style scoped>
/* Dùng lại y chang style của Login.vue */
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
  color: #e5e5e5;
  line-height: 1;
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

.error {
  color: red;
  font-size: 0.9em;
  margin-top: 5px;
}

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
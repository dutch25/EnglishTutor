<template>
  <div class="edit-profile-wrapper">
    <h1 class="profile-title">Sửa Hồ Sơ</h1>
    <div class="edit-profile-content">
      <div class="form-group">
        <label>Tên tài khoản:</label>
        <input v-model="username" type="text" />
      </div>
      <div class="form-group">
        <label>Email:</label>
        <input v-model="email" type="email" />
      </div>
      <div class="form-group">
        <label>Số điện thoại:</label>
        <input v-model="phone" type="text" />
      </div>
      <div class="form-group">
        <label>Mô tả bản thân:</label>
        <textarea v-model="description"></textarea>
      </div>

      <div class="button-group">
        <button @click="goBack" class="action-btn cancel-btn">❌ Hủy</button>
        <button @click="updateProfile" class="action-btn save-btn">💾 Lưu Thay Đổi</button>
      </div>

      <div v-if="errorMessage" class="toast error">{{ errorMessage }}</div>
      <div v-if="successMessage" class="toast success">{{ successMessage }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "EditProfile",
  data() {
    return {
      username: "",
      oldUsername: "",
      email: "",
      phone: "",
      description: "",
      errorMessage: "",
      successMessage: ""
    };
  },
  mounted() {
    const user = localStorage.getItem("username");
    if (!user) {
      this.$router.push("/");
    } else {
        this.oldUsername = user;
      fetch(`http://localhost:8000/api/user/${user}`)
        .then((res) => res.json())
        .then((data) => {
          this.username = user;
          this.email = data.email || "";
          this.phone = data.phone || "";
          this.description = data.description || "";
        })
        .catch((error) => {
          console.error("Error fetching user data:", error);
        });
    }
  },
  methods: {
    updateProfile() {
      this.errorMessage = "";
      this.successMessage = "";

      if (!this.username || !this.email) {
        this.errorMessage = "Tên tài khoản và email là bắt buộc!";
        return;
      }

      fetch("http://localhost:8000/api/user/update-profile", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          old_username: this.oldUsername,
          username: this.username,
          email: this.email,
          phone: this.phone,
          description: this.description
        }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.detail) {
            this.errorMessage = data.detail;
          } else {
            this.successMessage = "Cập nhật hồ sơ thành công!";
            if (this.username !== this.oldUsername) {
              localStorage.setItem("username", this.username);
            }
            setTimeout(() => {
              this.$router.push("/profile").then(() => {
                location.reload();
            });
            }, 1500);
          }
        })
        .catch((error) => {
          console.error("Error updating profile:", error);
          this.errorMessage = "Lỗi kết nối server!";
        });
    },
    goBack() {
      this.$router.push("/profile");
    }
  }
};
</script>

<style scoped>
.edit-profile-wrapper {
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

.edit-profile-content {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  padding: 30px;
  border-radius: 20px;
  width: 100%;
  max-width: 500px;
  box-sizing: border-box;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 6px;
}

.form-group input,
.form-group textarea {
  padding: 10px;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.3);
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
  box-sizing: border-box;
}

textarea {
  min-height: 100px;
  resize: vertical;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
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

.save-btn {
  background: linear-gradient(135deg, #00c6ff, #0072ff);
}

.cancel-btn {
  background: linear-gradient(135deg, #ff416c, #ff4b2b);
}

.toast {
  margin-top: 20px;
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
</style>

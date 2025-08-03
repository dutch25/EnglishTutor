<template>
  <div class="edit-profile-wrapper">
    <h1>Sửa Hồ Sơ</h1>
    <div class="form-container"> <!-- Thêm container này -->
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
        <button @click="updateProfile" class="save-btn">Lưu Thay Đổi</button>
        <button @click="goBack" class="cancel-btn">Hủy</button>
      </div>

      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
      <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
    </div> <!-- Kết thúc .form-container -->
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
  background-color: #1a1a2e;
  color: #ffffff;
  min-height: 100vh;
  padding: 40px 20px;
  font-family: "Segoe UI", sans-serif;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-container {
  background-color: #2a2a3d;
  padding: 30px;
  border-radius: 16px;
  border: 2px solid #2a2a3d; /* Border trắng */
  max-width: 500px;
  width: 100%;
  box-sizing: border-box;
}

.form-group {
  width: 100%;
  max-width: 500px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: bold;
  margin-bottom: 6px;
}

.form-group input,
.form-group textarea {
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  background-color: #2a2a3d;
  color: #fff;
}

textarea {
  min-height: 100px;
  resize: vertical;
}

.button-group {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 500px;
  margin-top: 20px;
}

.save-btn,
.cancel-btn {
  padding: 10px 20px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

.save-btn {
  background-color: #3b82f6;
  color: white;
}

.cancel-btn {
  background-color: #6c6c6c;
  color: white;
}

.error-message {
  color: #ff4d4f;
  margin-top: 20px;
}

.success-message {
  color: #52c41a;
  margin-top: 20px;
}
</style>

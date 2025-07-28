<template>
  <div class="ipa-wrapper">
    <h1 class="ipa-title">Bảng Phiên Âm IPA</h1>

    <div v-for="(group, groupIndex) in vowelGroups" :key="groupIndex" class="ipa-group">
      <h2 class="ipa-group-title">{{ group.title }}</h2>
      <div class="ipa-list">
        <div
          v-for="(sound, soundIndex) in group.list"
          :key="soundIndex"
          class="ipa-item"
        >
          <div class="ipa-phonetic">{{ sound.phonetic }}</div>
          <div class="ipa-desc">{{ sound.desc }}</div>
          <ul class="ipa-examples">
            <li v-for="(example, idx) in sound.examples" :key="idx">
              <strong>{{ example.word }}</strong>: {{ example.phonetic }}
            </li>
          </ul>
          <audio v-if="sound.audioSrc" :src="sound.audioSrc" controls class="audio-player" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import iShortAu from '@/assets/audios/ipa/vowels/i-short.mp3';
import iLongAu from '@/assets/audios/ipa/vowels/i-long.mp3';
import uShortAu from '@/assets/audios/ipa/vowels/u-short.mp3';
import uLongAu from '@/assets/audios/ipa/vowels/u-long.mp3';

export default {
  name: 'IPA',
  data() {
    return {
      vowelGroups: [
        {
          title: '😁 Nhóm âm cười',
          list: [
            {
              phonetic: 'ɪ',
              audioSrc: iShortAu,
              desc: 'i ngắn, đọc dứt khoát như đang kêu ai đó, miệng không căng',
              examples: [
                { word: 'ship', phonetic: '/ʃɪp/' },
                { word: 'hit', phonetic: '/hɪt/' },
              ],
            },
            {
              phonetic: 'i:',
              audioSrc: iLongAu,
              desc: 'i dài, miệng cười, nhấn mạnh, nặng và căng',
              examples: [
                { word: 'sheep', phonetic: '/ʃi:p/' },
                { word: 'heat', phonetic: '/hi:t/' },
              ],
            },
          ],
        },
        {
          title: '💋 Nhóm âm hôn',
          list: [
            {
              phonetic: 'ʊ',
              audioSrc: uShortAu,
              desc: 'u ngắn, tròn môi nhẹ, dứt khoát, không căng',
              examples: [
                { word: 'foot', phonetic: '/fʊt/' },
                { word: 'put', phonetic: '/pʊt/' },
              ],
            },
            {
              phonetic: 'u:',
              audioSrc: uLongAu,
              desc: 'u dài, chu và tròn môi, căng và mạnh',
              examples: [
                { word: 'blue', phonetic: '/blu:/' },
                { word: 'group', phonetic: '/gru:p/' },
              ],
            },
          ],
        },
      ],
    };
  },
};
</script>

<style scoped>
body {
  margin: 0;
  background-color: #1a1a2e;
}

.ipa-wrapper {
  max-width: 100%;
  padding: 2rem 1rem;
  background-color: #1a1a2e;
  color: #ffffff;
  font-family: 'Segoe UI', sans-serif;
  box-sizing: border-box;
}

.ipa-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 2rem;
}

.ipa-group {
  margin-bottom: 2.5rem;
}

.ipa-group-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #ffd369;
  text-align: center;
}

.ipa-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1.25rem;
}

.ipa-item {
  background-color: #2a2a3d;
  border-radius: 16px;
  padding: 1rem;
  width: 240px;
  box-shadow: 0 4px 12px rgba(255, 255, 255, 0.05);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.ipa-phonetic {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #ffffff;
}

.ipa-desc {
  font-size: 0.95rem;
  color: #b0b0c3;
  margin-bottom: 0.5rem;
}

.ipa-examples {
  list-style: none;
  padding: 0;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #e0e0e0;
}

.audio-player {
  width: 100%;
  margin-top: 0.5rem;
}
</style>

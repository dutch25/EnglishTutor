<template>
  <div class="ipa-page">
    <div class="ipa-wrapper">
    <button class="back-button" @click="goHome">
    ← Quay về trang chủ
    </button>
      <h1 class="ipa-title">Bảng Phiên Âm IPA (44 âm)</h1>

      <div v-for="(group, gIdx) in ipaGroups" :key="gIdx" class="ipa-group">
        <h2 class="ipa-group-title">{{ group.title }}</h2>
        <div class="ipa-list">
          <div v-for="(sound, sIdx) in group.list" :key="sIdx" class="ipa-item">
            <div class="ipa-phonetic">{{ sound.phonetic }}</div>
            <div class="ipa-desc">{{ sound.desc }}</div>
            <ul class="ipa-examples">
              <li v-for="(ex, eIdx) in sound.examples" :key="eIdx">
                <strong>{{ ex.word }}</strong
                >: {{ ex.phonetic }}
              </li>
            </ul>
            <audio
              v-if="sound.audioSrc"
              :src="sound.audioSrc"
              controls
              class="audio-player"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/* --- Import vowels audio --- */
import iShortAu from "@/assets/audios/ipa/vowels/i-short.mp3";
import iLongAu from "@/assets/audios/ipa/vowels/i-long.mp3";
import uShortAu from "@/assets/audios/ipa/vowels/u-short.mp3";
import uLongAu from "@/assets/audios/ipa/vowels/u-long.mp3";
import eAu from "@/assets/audios/ipa/vowels/e.mp3";
import aeAu from "@/assets/audios/ipa/vowels/ae.mp3";
import aaAu from "@/assets/audios/ipa/vowels/aa.mp3";
import aLongAu from "@/assets/audios/ipa/vowels/a-long.mp3";
import oAu from "@/assets/audios/ipa/vowels/o.mp3";
import oUkAu from "@/assets/audios/ipa/vowels/o-uk.mp3";
import owAu from "@/assets/audios/ipa/vowels/ow.mp3";
import owLongAu from "@/assets/audios/ipa/vowels/ow-long.mp3";

/* --- Import diphthongs audio --- */
import eiAu from "@/assets/audios/ipa/diphthongs/ei.mp3";
import aiAu from "@/assets/audios/ipa/diphthongs/ai.mp3";
import oiAu from "@/assets/audios/ipa/diphthongs/oi.mp3";
import auAu from "@/assets/audios/ipa/diphthongs/au.mp3";
import owuAu from "@/assets/audios/ipa/diphthongs/owu.mp3";
import iowAu from "@/assets/audios/ipa/diphthongs/iow.mp3";
import eowAu from "@/assets/audios/ipa/diphthongs/eow.mp3";
import uowAu from "@/assets/audios/ipa/diphthongs/uow.mp3";

export default {
  name: "IPA",
  data() {
    return {
      ipaGroups: [
        /* === Vowels (12) === */
        {
          title: "Nguyên âm đơn (Vowels)",
          list: [
            {
              phonetic: "ɪ",
              audioSrc: iShortAu,
              desc: "i ngắn",
              examples: [
                { word: "ship", phonetic: "/ʃɪp/" },
                { word: "hit", phonetic: "/hɪt/" },
              ],
            },
            {
              phonetic: "i:",
              audioSrc: iLongAu,
              desc: "i dài",
              examples: [
                { word: "sheep", phonetic: "/ʃi:p/" },
                { word: "heat", phonetic: "/hi:t/" },
              ],
            },
            {
              phonetic: "ʊ",
              audioSrc: uShortAu,
              desc: "u ngắn",
              examples: [
                { word: "foot", phonetic: "/fʊt/" },
                { word: "put", phonetic: "/pʊt/" },
              ],
            },
            {
              phonetic: "u:",
              audioSrc: uLongAu,
              desc: "u dài",
              examples: [
                { word: "blue", phonetic: "/blu:/" },
                { word: "group", phonetic: "/gru:p/" },
              ],
            },
            {
              phonetic: "e",
              audioSrc: eAu,
              desc: "e ngắn",
              examples: [
                { word: "ten", phonetic: "/ten/" },
                { word: "bed", phonetic: "/bed/" },
              ],
            },
            {
              phonetic: "æ",
              audioSrc: aeAu,
              desc: "ae",
              examples: [
                { word: "cat", phonetic: "/kæt/" },
                { word: "trap", phonetic: "/træp/" },
              ],
            },
            {
              phonetic: "ɑ:",
              audioSrc: aLongAu,
              desc: "a dài",
              examples: [
                { word: "father", phonetic: "/ˈfɑ:ðər/" },
                { word: "arm", phonetic: "/ɑ:m/" },
              ],
            },
            {
              phonetic: "ɒ",
              audioSrc: oUkAu,
              desc: "o ngắn",
              examples: [
                { word: "got", phonetic: "/ɡɒt/" },
                { word: "shot", phonetic: "/ʃɒt/" },
              ],
            },
            {
              phonetic: "ɔ:",
              audioSrc: oAu,
              desc: "o dài",
              examples: [
                { word: "law", phonetic: "/lɔ:/" },
                { word: "thought", phonetic: "/θɔ:t/" },
              ],
            },
            {
              phonetic: "ʌ",
              audioSrc: aaAu,
              desc: "â",
              examples: [
                { word: "cup", phonetic: "/kʌp/" },
                { word: "drum", phonetic: "/drʌm/" },
              ],
            },
            {
              phonetic: "ɜ:",
              audioSrc: owLongAu,
              desc: "ơ dài",
              examples: [
                { word: "bird", phonetic: "/bɜ:d/" },
                { word: "nurse", phonetic: "/nɜ:s/" },
              ],
            },
            {
              phonetic: "ə",
              audioSrc: owAu,
              desc: "schwa",
              examples: [
                { word: "ago", phonetic: "/əˈɡəʊ/" },
                { word: "teacher", phonetic: "/ˈti:tʃə/" },
              ],
            },
          ],
        },

        /* === Diphthongs (8) === */
        {
          title: "Nguyên âm đôi (Diphthongs)",
          list: [
            {
              phonetic: "eɪ",
              audioSrc: eiAu,
              desc: "êi",
              examples: [
                { word: "say", phonetic: "/seɪ/" },
                { word: "day", phonetic: "/deɪ/" },
              ],
            },
            {
              phonetic: "aɪ",
              audioSrc: aiAu,
              desc: "ai",
              examples: [
                { word: "five", phonetic: "/faɪv/" },
                { word: "sky", phonetic: "/skaɪ/" },
              ],
            },
            {
              phonetic: "ɔɪ",
              audioSrc: oiAu,
              desc: "oi",
              examples: [
                { word: "boy", phonetic: "/bɔɪ/" },
                { word: "join", phonetic: "/dʒɔɪn/" },
              ],
            },
            {
              phonetic: "aʊ",
              audioSrc: auAu,
              desc: "ao",
              examples: [
                { word: "house", phonetic: "/haʊs/" },
                { word: "flower", phonetic: "/ˈflaʊə/" },
              ],
            },
            {
              phonetic: "əʊ",
              audioSrc: owuAu,
              desc: "âu",
              examples: [
                { word: "home", phonetic: "/həʊm/" },
                { word: "go", phonetic: "/ɡəʊ/" },
              ],
            },
            {
              phonetic: "ɪə",
              audioSrc: iowAu,
              desc: "iơ",
              examples: [
                { word: "here", phonetic: "/hɪə/" },
                { word: "near", phonetic: "/nɪə/" },
              ],
            },
            {
              phonetic: "eə",
              audioSrc: eowAu,
              desc: "eơ",
              examples: [
                { word: "care", phonetic: "/keə/" },
                { word: "hair", phonetic: "/heə/" },
              ],
            },
            {
              phonetic: "ʊə",
              audioSrc: uowAu,
              desc: "uơ",
              examples: [
                { word: "tour", phonetic: "/tʊə/" },
                { word: "pure", phonetic: "/pjʊə/" },
              ],
            },
          ],
        },

        /* === Consonants (24) === */
        {
          title: "Phụ âm (Consonants)",
          list: [
            {
              phonetic: "p",
              audioSrc: null,
              desc: "p bật hơi",
              examples: [
                { word: "pen", phonetic: "/pen/" },
                { word: "happy", phonetic: "/ˈhæpi/" },
              ],
            },
            {
              phonetic: "b",
              audioSrc: null,
              desc: "b hữu thanh",
              examples: [
                { word: "bat", phonetic: "/bæt/" },
                { word: "job", phonetic: "/dʒɒb/" },
              ],
            },
            {
              phonetic: "t",
              audioSrc: null,
              desc: "t vô thanh",
              examples: [
                { word: "tea", phonetic: "/ti:/" },
                { word: "stop", phonetic: "/stɒp/" },
              ],
            },
            {
              phonetic: "d",
              audioSrc: null,
              desc: "d hữu thanh",
              examples: [
                { word: "dog", phonetic: "/dɒg/" },
                { word: "ladder", phonetic: "/ˈlædə/" },
              ],
            },
            {
              phonetic: "k",
              audioSrc: null,
              desc: "k vô thanh",
              examples: [
                { word: "cat", phonetic: "/kæt/" },
                { word: "back", phonetic: "/bæk/" },
              ],
            },
            {
              phonetic: "g",
              audioSrc: null,
              desc: "g hữu thanh",
              examples: [
                { word: "go", phonetic: "/gəʊ/" },
                { word: "bag", phonetic: "/bæg/" },
              ],
            },
            {
              phonetic: "f",
              audioSrc: null,
              desc: "f vô thanh",
              examples: [
                { word: "fish", phonetic: "/fɪʃ/" },
                { word: "safe", phonetic: "/seɪf/" },
              ],
            },
            {
              phonetic: "v",
              audioSrc: null,
              desc: "v hữu thanh",
              examples: [
                { word: "voice", phonetic: "/vɔɪs/" },
                { word: "save", phonetic: "/seɪv/" },
              ],
            },
            {
              phonetic: "θ",
              audioSrc: null,
              desc: "th vô thanh",
              examples: [
                { word: "think", phonetic: "/θɪŋk/" },
                { word: "thank", phonetic: "/θæŋk/" },
              ],
            },
            {
              phonetic: "ð",
              audioSrc: null,
              desc: "th hữu thanh",
              examples: [
                { word: "this", phonetic: "/ðɪs/" },
                { word: "mother", phonetic: "/ˈmʌðə/" },
              ],
            },
            {
              phonetic: "s",
              audioSrc: null,
              desc: "s vô thanh",
              examples: [
                { word: "see", phonetic: "/si:/" },
                { word: "rice", phonetic: "/raɪs/" },
              ],
            },
            {
              phonetic: "z",
              audioSrc: null,
              desc: "z hữu thanh",
              examples: [
                { word: "zoo", phonetic: "/zu:/" },
                { word: "rose", phonetic: "/rəʊz/" },
              ],
            },
            {
              phonetic: "ʃ",
              audioSrc: null,
              desc: "sh vô thanh",
              examples: [
                { word: "she", phonetic: "/ʃi:/" },
                { word: "wash", phonetic: "/wɒʃ/" },
              ],
            },
            {
              phonetic: "ʒ",
              audioSrc: null,
              desc: "giơ hữu thanh",
              examples: [
                { word: "vision", phonetic: "/ˈvɪʒən/" },
                { word: "measure", phonetic: "/ˈmeʒə/" },
              ],
            },
            {
              phonetic: "h",
              audioSrc: null,
              desc: "h vô thanh",
              examples: [
                { word: "hat", phonetic: "/hæt/" },
                { word: "hello", phonetic: "/həˈləʊ/" },
              ],
            },
            {
              phonetic: "tʃ",
              audioSrc: null,
              desc: "ch",
              examples: [
                { word: "check", phonetic: "/tʃek/" },
                { word: "church", phonetic: "/tʃɜ:tʃ/" },
              ],
            },
            {
              phonetic: "dʒ",
              audioSrc: null,
              desc: "j",
              examples: [
                { word: "job", phonetic: "/dʒɒb/" },
                { word: "juice", phonetic: "/dʒu:s/" },
              ],
            },
            {
              phonetic: "m",
              audioSrc: null,
              desc: "m",
              examples: [
                { word: "man", phonetic: "/mæn/" },
                { word: "some", phonetic: "/sʌm/" },
              ],
            },
            {
              phonetic: "n",
              audioSrc: null,
              desc: "n",
              examples: [
                { word: "no", phonetic: "/nəʊ/" },
                { word: "button", phonetic: "/ˈbʌtn/" },
              ],
            },
            {
              phonetic: "ŋ",
              audioSrc: null,
              desc: "ng",
              examples: [
                { word: "sing", phonetic: "/sɪŋ/" },
                { word: "song", phonetic: "/sɒŋ/" },
              ],
            },
            {
              phonetic: "l",
              audioSrc: null,
              desc: "l",
              examples: [
                { word: "leg", phonetic: "/leg/" },
                { word: "call", phonetic: "/kɔ:l/" },
              ],
            },
            {
              phonetic: "r",
              audioSrc: null,
              desc: "r",
              examples: [
                { word: "red", phonetic: "/red/" },
                { word: "car", phonetic: "/kɑ:/" },
              ],
            },
            {
              phonetic: "j",
              audioSrc: null,
              desc: "j (y)",
              examples: [
                { word: "yes", phonetic: "/jes/" },
                { word: "yellow", phonetic: "/ˈjeləʊ/" },
              ],
            },
            {
              phonetic: "w",
              audioSrc: null,
              desc: "w",
              examples: [
                { word: "we", phonetic: "/wi:/" },
                { word: "window", phonetic: "/ˈwɪndəʊ/" },
              ],
            },
          ],
        },
      ],
    };
  },
  methods: {
  goHome() {
  this.$router.push("/home");
  },
  },
  };

</script>

<style scoped>
.ipa-page {
  background-image: url('../assets/images/background.jpg');
  background-size: cover;
  background-position: center;
}

.ipa-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  color: #ffffff;
  font-family: "Segoe UI", sans-serif;
  position: relative;
  z-index: 1;
}

.ipa-title {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 2rem;
  background: linear-gradient(90deg, #3b3b3b, #19191a);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 6px rgba(0, 0, 0, 0.5);
}

.ipa-group {
  margin-bottom: 2.5rem;
}

.ipa-group-title {
  text-align: center;
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #616503;
  text-shadow: 0 1px 3px rgba(0, 0, 0, 0.4);
}

/* Danh sách âm */
.ipa-list {
  display: grid;
  grid-template-columns: repeat(4, 1fr); /* 4 ô 1 hàng */
  gap: 1.5rem;
  justify-items: center;
}

/* Responsive: Xuống 3 ô, 2 ô, 1 ô nếu màn nhỏ */
@media (max-width: 1024px) {
  .ipa-list {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .ipa-list {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .ipa-list {
    grid-template-columns: repeat(1, 1fr);
  }
}

/* Box IPA Item */
.ipa-item {
  background: rgba(30, 30, 45, 0.9); /* Tối hơn */
  backdrop-filter: blur(6px);
  border-radius: 20px;
  padding: 1rem;
  width: 100%;
  max-width: 240px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.ipa-item:hover {
  transform: translateY(-6px);
  box-shadow: 0 0 20px rgba(255, 211, 105, 0.5);
}

.ipa-phonetic {
  font-size: 1.6rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.ipa-desc {
  font-size: 0.9rem;
  color: #b0b0c3;
  margin-bottom: 0.5rem;
}

.ipa-examples {
  list-style: none;
  padding: 0;
  margin: 0 0 0.5rem;
  font-size: 0.85rem;
  color: #e0e0e0;
}

.ipa-examples li {
  margin-bottom: 0.2rem;
}

.audio-player {
  width: 100%;
  margin-top: 0.5rem;
  filter: brightness(0.9);
}

.back-button {
  background: rgba(255, 255, 255, 0.1);
  color: #23234b;
  font-size: 14px;
  padding: 8px 16px;
  margin-bottom: 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.2s;
}
.back-button:hover {
background:#97b368;
  color: #fff;
}
</style>

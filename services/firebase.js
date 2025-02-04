// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyD_BEI1JBczck5ND13jRVdMc1ix8JVR9-E",
  authDomain: "serviceshomebackend.firebaseapp.com",
  projectId: "serviceshomebackend",
  storageBucket: "serviceshomebackend.firebasestorage.app",
  messagingSenderId: "439283222861",
  appId: "1:439283222861:web:54e81975fa0c262d078f04",
  measurementId: "G-WY96FKRC3D"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
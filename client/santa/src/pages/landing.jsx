import React from "react";
import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-r from-purple-400 via-pink-500 to-red-500 flex flex-col items-center justify-center text-white">
      <h1 className="text-5xl font-bold mb-6">Welcome to Santa Link 🎅</h1>
      <p className="text-xl mb-8 text-center max-w-xl">
        Connect with friends, family, and colleagues to exchange gifts in a fun and anonymous way!
      </p>
      <div className="flex gap-4">
        <Link 
          to="/create-group" 
          className="bg-white text-red-500 font-semibold px-6 py-3 rounded-lg shadow-lg hover:bg-gray-100 transition">
          Create a Group
        </Link>
        <Link 
          to="/join" 
          className="bg-white text-red-500 font-semibold px-6 py-3 rounded-lg shadow-lg hover:bg-gray-100 transition">
          Join a Group
        </Link>
      </div>
      <footer className="absolute bottom-4 text-sm opacity-70">
        &copy; 2025 Santa Link. All rights reserved.
      </footer>
    </div>
  );
}

<template>
  <div class="home-page">
    <h1>Welcome to Planeswalkers Grimoire</h1>
    <p>
      <strong>Planeswalkers Grimoire</strong> is your personal Magic: The Gathering collection and deck manager.
    </p>
    <div class="disclaimer">
      <strong>Note:</strong> This project is in its early stages. Features and design are actively being developed and may change frequently.
    </div>
    <ul>
      <li>Track and organize your entire MTG card collection.</li>
      <li>Build, edit, and manage your decks with ease.</li>
      <li>Analyze your collection and decks against current meta and competitive decks.</li>
      <li>Discover gaps in your collection and optimize your builds for competitive play.</li>
    </ul>
    <p>
      Get started by logging in and exploring your collection or decks!
    </p>
  </div>
</template>

<style scoped>
.home-page {
  max-width: 700px;
  margin: 40px auto;
  background: rgba(255,255,255,0.97);
  border-radius: 10px;
  padding: 2em;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  text-align: center;
  color: #222; /* <-- Add this line for dark text */
}
.home-page h1 {
  margin-bottom: 1em;
}
.home-page ul {
  text-align: left;
  margin: 1em auto 2em auto;
  max-width: 500px;
}
.disclaimer {
  background: #fff3cd;
  color: #856404;
  border: 1px solid #ffeeba;
  border-radius: 6px;
  padding: 0.8em 1em;
  margin: 1em 0 2em 0;
  font-size: 1.05em;
}
</style>
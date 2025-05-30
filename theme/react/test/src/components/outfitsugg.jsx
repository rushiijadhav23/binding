import React from "react";
import "../css/styles.css";

export function OutfitSuggestion({ outfitData }) {
  if (!outfitData || !outfitData.length) return null;

  return (
    <div className="outfit-container">
      <h2>Complete Your Outfit</h2>
      <div className="outfit-grid">
        {outfitData.map((item) => (
          <div key={item.slug} className="outfit-card">
            <img src={item.media?.[0]?.url} alt={item.name} className="outfit-img" />
            <h4>{item.name}</h4>
            <p>₹ {item.price?.effective?.min}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

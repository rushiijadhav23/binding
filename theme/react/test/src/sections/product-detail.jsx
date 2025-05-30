import React, { useEffect, useState } from "react";
import { useFPI, useGlobalStore } from "fdk-core/utils";
import { OutfitSuggestion } from "../components/OutfitSuggestion";
import { fetchMetadataFromGemini } from "../utils/gemini-api";
import "../css/styles.css";

const PRODUCT_QUERY = `query {
  product {
    name
    slug
    media { url }
    price { effective { min } }
    description
    category {
      name
    }
  }
}`;

const OUTFIT_QUERY = `
  query product_search($filters: ProductFiltersInput) {
    product_search(filters: $filters) {
      items {
        name
        slug
        media { url }
        price { effective { min } }
      }
    }
  }
`;

export function Component() {
  const fpi = useFPI();
  const [currentProduct, setCurrentProduct] = useState(null);
  const [outfitData, setOutfitData] = useState([]);

  useEffect(() => {
    fpi.executeGQL(PRODUCT_QUERY).then((res) => {
      const product = res?.product;
      setCurrentProduct(product);

      if (product) {
        fetchMetadataFromGemini(product).then((metadata) => {
          if (metadata) {
            const filters = {
              tags: metadata.tags,
              category: metadata.suggested_categories,
              gender: metadata.gender,
            };
            fpi.executeGQL(OUTFIT_QUERY, { filters }).then((outfitRes) => {
              setOutfitData(outfitRes?.product_search?.items || []);
            });
          }
        });
      }
    });
  }, [fpi]);

  if (!currentProduct) return <h2>Loading Product...</h2>;

  return (
    <div>
      <h1>{currentProduct.name}</h1>
      <img src={currentProduct.media?.[0]?.url} alt={currentProduct.name} width="200" />
      <p>{currentProduct.description}</p>
      <h3>₹ {currentProduct.price?.effective?.min}</h3>

      {/* Outfit Suggestions */}
      <OutfitSuggestion outfitData={outfitData} />
    </div>
  );
}

"use client";

import Image from "next/image";
import { MasonryGrid } from "@once-ui-system/core";

interface GalleryViewProps {
  images: string[];
}

export default function GalleryView({ images }: GalleryViewProps) {
  return (
    <MasonryGrid columns={2} s={{ columns: 1 }}>
      {images.map((src, index) => (
        <div key={index} style={{ width: "100%", borderRadius: "var(--radius-m)", overflow: "hidden" }}>
          <Image
            src={src}
            alt={`gallery-${index + 1}`}
            width={0}
            height={0}
            sizes="(max-width: 560px) 100vw, 50vw"
            style={{ width: "100%", height: "auto", display: "block" }}
            priority={index < 6}
          />
        </div>
      ))}
    </MasonryGrid>
  );
}

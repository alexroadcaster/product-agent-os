import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  images: {
    remotePatterns: [
      {
        hostname: "api.iconify.design",
        protocol: "https",
      },
    ],
  },
  reactCompiler: true,
};

export default nextConfig;

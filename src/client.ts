import dgram from "node:dgram";
import fs from "node:fs";

const server = dgram.createSocket("udp4");
const writer = fs.createWriteStream("dist/video.h265");

server.on("error", (err) => {
  console.error(`server error:\n${err.stack}`);
  server.close();
  writer.end(() => {
    writer.close();
  });
});

server.on("message", (msg, rinfo) => {
  console.log("👍 packet received " + msg.length.toLocaleString());
  writer.write(msg);
});

server.on("listening", () => {
  const address = server.address();
  console.log(`server listening ${address.address}:${address.port}`);
});

server.bind(5005);
// Prints: server listening 0.0.0.0:5005

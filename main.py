import { rootServer, RootBotStartState } from "@rootsdk/server-bot";

interface Song {
  title: string;
  requestedBy: string;
}

const queue: Song[] = [];
let isPlaying = false;

// Funkcja startowa
async function onStarting(state: RootBotStartState) {
  console.log("🤖 DJ Norbert Bot został pomyślnie uruchomiony!");
}

// Rejestracja obsługi wiadomości
if (rootServer && typeof rootServer.on === "function") {
  rootServer.on("message", async (msg: any) => {
    const text = msg.content?.trim();
    if (!text || !text.startsWith("!")) return;

    const args = text.slice(1).split(" ");
    const command = args.shift()?.toLowerCase();

    // Komenda !play
    if (command === "play") {
      const songQuery = args.join(" ");
      if (!songQuery) {
        if (typeof msg.reply === "function") {
          await msg.reply("❌ Podaj nazwę utworu! Użycie: `!play Nazwa Piosenki`");
        }
        return;
      }

      const newSong: Song = {
        title: songQuery,
        requestedBy: msg.author?.username || "Użytkownik",
      };

      queue.push(newSong);

      if (!isPlaying) {
        isPlaying = true;
        if (typeof msg.reply === "function") {
          await msg.reply(`🎶 **Odtwarzam teraz:** ${newSong.title} (zamówił: ${newSong.requestedBy})`);
        }
      } else {
        if (typeof msg.reply === "function") {
          await msg.reply(`🎵 **Dodano do kolejki (#${queue.length}):** ${newSong.title}`);
        }
      }
    }

    // Komenda !skip
    if (command === "skip") {
      if (queue.length === 0) {
        if (typeof msg.reply === "function") {
          await msg.reply("❌ Kolejka jest pusta!");
        }
        return;
      }

      const skipped = queue.shift();
      if (queue.length > 0) {
        if (typeof msg.reply === "function") {
          await msg.reply(`⏭️ Pominięto **${skipped?.title}**. Teraz gra: **${queue[0].title}**`);
        }
      } else {
        isPlaying = false;
        if (typeof msg.reply === "function") {
          await msg.reply(`⏭️ Pominięto **${skipped?.title}**. Kolejka jest pusta.`);
        }
      }
    }

    // Komenda !queue
    if (command === "queue" || command === "kolejka") {
      if (queue.length === 0) {
        if (typeof msg.reply === "function") {
          await msg.reply("📋 Kolejka jest pusta. Dodaj coś za pomocą `!play`!");
        }
        return;
      }

      let queueList = "🎶 **Obecna kolejka:**\n";
      queue.forEach((song, index) => {
        queueList += `${index + 1}. **${song.title}** (zamówił: ${song.requestedBy})\n`;
      });

      if (typeof msg.reply === "function") {
        await msg.reply(queueList);
      }
    }

    // Komenda !help
    if (command === "help") {
      if (typeof msg.reply === "function") {
        await msg.reply(
          "🎧 **DJ Norbert Bot - Komendy:**\n" +
          "• `!play <tytuł>` - dodaje utwór do kolejki\n" +
          "• `!skip` - pomija aktualny utwór\n" +
          "• `!queue` - lista utworów\n" +
          "• `!help` - pomoc"
        );
      }
    }
  });
}

// Uruchomienie cyklu życia bota
(async () => {
  try {
    await rootServer.lifecycle.start(onStarting);
  } catch (error) {
    console.error("Błąd podczas uruchamiania bota:", error);
  }
})();

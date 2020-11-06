import org.json.JSONObject;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.Random;
import java.util.concurrent.CompletableFuture;

public final class MiniMinerSolution {
    public static final String ENCODED_TOKEN = "233333%3AMEUCIQDTTJu25fXbAgKcF%2BMDCGp1OSTd%2B4OwvNmTn%2FDhZryCiAIgDQXsmAHvLrAe2BSwaoSZO%2Bml6as%2BAj0N51PI3e6Befs";
    public static final String DAMAGE_URL = "http://localhost:10169/api/damage?&x={0}&y={1}&material=DIAMOND&token=" + ENCODED_TOKEN;
    public static final String STATE_URL = "http://localhost:10169/api/state?x=0&y=0&token=" + ENCODED_TOKEN;
    public static final String RESET_URL = "http://localhost:10169/api/reset?token=" + ENCODED_TOKEN;

    public static void main(String[] args) throws Exception {
        var client = HttpClient.newHttpClient();

        // reset

        var body = HttpRequest.BodyPublishers.noBody();
        var resetReq = HttpRequest.newBuilder(new URI(RESET_URL)).POST(body).build();
        client.send(resetReq, HttpResponse.BodyHandlers.discarding());

        System.out.println("Request: " + RESET_URL);

        // get state

        var stateReq = HttpRequest.newBuilder(new URI(STATE_URL)).GET().build();
        var state = new JSONObject(client.send(stateReq, HttpResponse.BodyHandlers.ofString()).body());

        System.out.println("Request: " + STATE_URL);

        // handle state

        var materials = new int[32][32];
        for (var i = 0; i < 32; i++) {
            for (var j = 0; j < 32; j++) {
                switch (state.getJSONArray("materials").getJSONArray(i).getString(j)) {
                    case "FLAG":
                        materials[i][j] = 5;
                        break;
                    case "OBSIDIAN":
                        materials[i][j] = 4;
                        break;
                    case "DIAMOND":
                        materials[i][j] = 3;
                        break;
                    case "IRON":
                        materials[i][j] = 2;
                        break;
                }
            }
        }

        // collide lower seed

        var rng = new Random();
        var lowerSeeds = new ArrayList<Long>();
        for (var lowerSeed = 0L; lowerSeed < 0x100000L; ++lowerSeed) {
            if (testSeed(rng, lowerSeed, materials, 16, 16, 4) && testSeed(rng, lowerSeed, materials, 16, 32, 3)) {
                lowerSeeds.add(lowerSeed);
            }
        }

        var step = 0;
        var total = lowerSeeds.size() * 256 + 1;
        System.out.println("Collision: step " + ++step + " of " + total);

        // collide the whole seed

        var seeds = new ArrayList<Long>();
        for (var lowerSeed : lowerSeeds) {
            for (var mediumSeed = 0L; mediumSeed < 0x100L; ++mediumSeed) {
                for (var upperSeed = 0L; upperSeed < 0x100000L; ++upperSeed) {
                    var seed = (upperSeed * 0x100L + mediumSeed) * 0x100000L + lowerSeed;
                    if (testSeed(rng, seed, materials, 48, 16, 4) && testSeed(rng, seed, materials, 48, 32, 3)) {
                        seeds.add(seed);
                    }
                }
                System.out.println("Collision: step " + ++step + " of " + total);
            }
        }

        System.out.println("Collided seeds: " + seeds);

        // damage possible flag locations

        var nextSeeds = new ArrayList<Long>();
        for (var seed : seeds) {
            nextSeeds.add(seed * 8);
            nextSeeds.add(seed * 8 + 1);
            nextSeeds.add(seed * 8 + 2);
            nextSeeds.add(seed * 8 + 3);
            nextSeeds.add(seed * 8 + 4);
            nextSeeds.add(seed * 8 + 5);
            nextSeeds.add(seed * 8 + 6);
            nextSeeds.add(seed * 8 + 7);
        }

        var futures = new ArrayList<CompletableFuture<?>>();
        for (var nextSeed : nextSeeds) {
            var chunkX = -1;
            var x = 0x1800000;
            var y = 0x1800000;
            while (x >= 0x1000000 || y >= 0x1000000) {
                rng.setSeed(nextSeed ^ (5 + 0x6E5D5AF15FA1280BL * ++chunkX));
                rng.nextInt();
                rng.nextInt();
                x = Math.floorMod(rng.nextInt() + chunkX + 1, 0x1800000);
                y = Math.floorMod(rng.nextInt() + 1, 0x1800000);
            }
            var damageUrlForSeed = MessageFormat.format(DAMAGE_URL, Integer.toString(x + 0x1000000 * chunkX), Integer.toString(y));
            var damageReq = HttpRequest.newBuilder(new URI(damageUrlForSeed)).POST(body).build();
            futures.add(client.sendAsync(damageReq, HttpResponse.BodyHandlers.ofString()).thenAccept(b -> {
                var damaged = new JSONObject(b.body());
                if ("FLAG".equals(damaged.getString("dropped"))) {
                    System.out.println("Flag: " + damaged.getString("flag"));
                }
            }));
            System.out.println("Request: " + damageUrlForSeed);
        }

        // wait for 1 second and reset again

        Thread.sleep(1000);

        client.send(resetReq, HttpResponse.BodyHandlers.discarding());
        System.out.println("Request: " + RESET_URL);
        futures.forEach(CompletableFuture::join);
    }

    private static boolean testSeed(Random rng, long seed, int[][] materials, int modular, int count, int ordinal) {
        var testMaterials = new boolean[modular][modular];
        rng.setSeed(seed ^ ordinal);
        for (var j = 0; j < count; ++j) {
            var randomX = Math.floorMod(rng.nextInt() * ((1 << j) - 1) + 1, modular);
            var randomY = Math.floorMod(rng.nextInt() * ((1 << j) - 1) + 1, modular);
            testMaterials[randomX][randomY] = true;
        }
        for (var i = 0; i < 32; ++i) {
            for (var j = 0; j < 32; ++j) {
                if (materials[i][j] == ordinal && !testMaterials[i % modular][j % modular]) {
                    return false;
                }
            }
        }
        return true;
    }
}

#include <SFML/Config.hpp>
#include <SFML/Graphics.hpp>
#include <SFML/Window/Keyboard.hpp>
#include <iostream>
#include <vector>
#include "PerlinNoise.h"

const uint16_t MAP_SIZE = 750;
const uint32_t SEED = 69420;

std::vector<std::vector<double>> getNoiseMap(const uint16_t mapSize,
                                             const uint32_t seed,
                                             const double noiseScale)
{
    PerlinNoise noise(seed);

    std::vector<std::vector<double>> map(mapSize, std::vector<double>(mapSize));

    for (int y = 0; y < mapSize; ++y)
    {
        for (int x = 0; x < mapSize; ++x)
        {
            double sampleX = x / noiseScale;
            double sampleY = y / noiseScale;

            double noiseValue = noise.noise(sampleX, sampleY, 0);

            map[x][y] = noiseValue;
        }
    }

    return map;
}

sf::Sprite regenerateMap(sf::Texture &texture, const double noiseScale)
{
    std::vector<std::vector<double>> noiseMap = getNoiseMap(MAP_SIZE, SEED, noiseScale);
    sf::Uint8 *pixels = new sf::Uint8[750 * 750 * 4];

    // Create pixel array
    for (int y = 0; y < 750; ++y)
    {
        for (int x = 0; x < 750; ++x)
        {
            int index = (x + y * 750) * 4;

            sf::Uint8 colorValue = 255 * noiseMap[x][y];
            pixels[index] = colorValue;
            pixels[index + 1] = colorValue;
            pixels[index + 2] = colorValue;
            pixels[index + 3] = 255;

            // pixels[index] = 255;
            // pixels[index + 1] = 255;
            // pixels[index + 2] = 255;
            // pixels[index + 3] = 255 * noiseMap[x][y];
        }
    }

    sf::Image image;
    image.create(750, 750, pixels);
    texture.loadFromImage(image);
    sf::Sprite sprite;
    sprite.setTexture(texture);

    return sprite;
}

int main()
{
    sf::RenderWindow window(sf::VideoMode(1250, 750), "Noise Visualizer", sf::Style::Titlebar | sf::Style::Close);

    double currentNoiseScale = 50;
    sf::Texture texture;
    sf::Sprite sprite = regenerateMap(texture, currentNoiseScale);

    while (window.isOpen())
    {
        // Get events
        sf::Event event;
        while (window.pollEvent(event))
        {
            switch (event.type)
            {
            case sf::Event::Closed:
                window.close();
            }
        }

        // Get inputs
        if (sf::Keyboard::isKeyPressed(sf::Keyboard::Up))
        {
            std::cout << currentNoiseScale << '\n';
            currentNoiseScale += 0.1;
            sprite = regenerateMap(texture, currentNoiseScale);
        }
        else if (sf::Keyboard::isKeyPressed(sf::Keyboard::Down))
        {
            std::cout << currentNoiseScale << '\n';
            currentNoiseScale -= 0.1;
            sprite = regenerateMap(texture, currentNoiseScale);
        }

        // Draw
        window.clear(sf::Color::Black);
        window.draw(sprite);
        window.display();
    }

    return 0;
}

#include <SFML/Config.hpp>
#include <SFML/Graphics.hpp>

#include "Label.hpp"
#include "PerlinNoise.hpp"
#include "Slider.hpp"

#include <cstdint>
#include <iostream>
#include <vector>

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
    std::vector<std::vector<double>> noiseMap = getNoiseMap(750, 69, noiseScale);
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
    // Create window
    sf::RenderWindow window(sf::VideoMode(1250, 750), "Noise Visualizer", sf::Style::Titlebar | sf::Style::Close);

    // Define fonts and colors
    sf::Font consolasFont;
    if (!consolasFont.loadFromFile("../assets/consola.ttf"))
    {
        throw "Font not loaded";
    }

    sf::Color black(0, 0, 0);
    sf::Color white(255, 255, 255);
    sf::Color gray(128, 128, 128);

    // Create textures
    double currentNoiseScale = 50;
    sf::Texture texture;
    sf::Sprite sprite = regenerateMap(texture, currentNoiseScale);

    // Create ui widgets
    Label scaleLabel(775, 10, "Noise Scale:", consolasFont, 30, white);
    Label scaleValueLabel(1000, 10, "50", consolasFont, 30, white);
    Slider scaleSlider(775, 70, 450, 10, 30, 20, 1, 100, 50, white, gray);

    while (window.isOpen())
    {
        // Get events
        sf::Event event;
        if (window.pollEvent(event))
        {
            switch (event.type)
            {
            case sf::Event::Closed:
                window.close();
                break;

            default:
                break;
            }
        }

        // Get slider value to update label
        if (scaleSlider.valueChanged())
        {
            double currentNoiseScale = scaleSlider.getValue();
            scaleValueLabel.setText(std::to_string(currentNoiseScale));
            regenerateMap(texture, currentNoiseScale);
        }

        // Draw (not tie, it means Render)
        window.clear(sf::Color::Black);

        window.draw(sprite);

        scaleValueLabel.draw(window);
        scaleLabel.draw(window);
        scaleSlider.draw(window);

        window.display();
    }

    return 0;
}

#include <SFML/Config.hpp>
#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>
#include <TGUI/TGUI.hpp>

#include "PerlinNoise.hpp"

#include <cmath>
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

void regenerateMap(sf::Image &image, sf::Texture &texture, sf::Sprite &sprite, double noiseScale)
{
    std::vector<std::vector<double>> noiseMap = getNoiseMap(500, 69, noiseScale);

    // Update pixels
    for (int y = 0; y < 500; ++y)
    {
        for (int x = 0; x < 500; ++x)
        {
            sf::Color color(255, 255, 255, 255 * noiseMap[x][y]);
            image.setPixel(x, y, color);
        }
    }

    texture.update(image);
    sprite.setTexture(texture);
}

void create_widgets(tgui::GuiSFML &gui)
{
    tgui::Theme::setDefault("../assets/Black.txt");

    tgui::Label::Ptr scaleLabel = tgui::Label::create();
    scaleLabel->setText("Noise scale:");
    scaleLabel->setTextSize(14);
    scaleLabel->setPosition(10, 10);
    gui.add(scaleLabel);
}

int main()
{
    ////////////////////////////////////////////////////////////
    // Define colors
    ////////////////////////////////////////////////////////////
    const sf::Color black(0, 0, 0);
    const sf::Color white(255, 255, 255);
    const sf::Color gray(128, 128, 128);

    ////////////////////////////////////////////////////////////
    // Create window
    ////////////////////////////////////////////////////////////
    sf::RenderWindow window;
    window.create(sf::VideoMode(750, 500), "Noise Visualizer", sf::Style::Titlebar | sf::Style::Close);

    ////////////////////////////////////////////////////////////
    // Create gui manager
    ////////////////////////////////////////////////////////////
    tgui::GuiSFML gui;
    gui.setTarget(window);
    gui.setFont(tgui::Font("../assets/consola.ttf"));

    create_widgets(gui);

    ////////////////////////////////////////////////////////////
    // Create textures
    ////////////////////////////////////////////////////////////
    double currentNoiseScale = 50;

    sf::Image image;
    image.create(750, 750, black);
    sf::Texture texture;
    texture.loadFromImage(image);
    sf::Sprite sprite;
    sprite.setPosition(250, 0);

    regenerateMap(image, texture, sprite, currentNoiseScale);

    ////////////////////////////////////////////////////////////
    // Main loop
    ////////////////////////////////////////////////////////////
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

        window.clear(black);
        window.draw(sprite);

        gui.draw();
        window.display();
    }

    return 0;
}

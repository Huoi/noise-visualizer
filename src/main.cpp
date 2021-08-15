#include <SFML/Graphics.hpp>
#include <TGUI/TGUI.hpp>

#include "PerlinNoise.hpp"

#include <cstdint>
#include <iostream>
#include <string>
#include <vector>

#define MAP_WIDTH 250
#define MAP_HEIGHT 250

#define BLACK sf::Color(0, 0, 0)
#define WHITE sf::Color(255, 255, 255)

#define MIN_NOISE_SCALE 1.0
#define MAX_NOISE_SCALE 100.0
#define DEFAULT_NOISE_SCALE 10.0

namespace tg = tgui;

struct NoiseMap
{
    sf::Image image;
    sf::Texture texture;
    sf::Sprite sprite;
};

NoiseMap map;

void regenerateNoise(NoiseMap &map, double noiseScale)
{
    PerlinNoise noise(69);

    for (uint16_t y = 0; y < MAP_HEIGHT; ++y)
    {
        for (uint16_t x = 0; x < MAP_WIDTH; ++x)
        {
            double sampleX = x / noiseScale;
            double sampleY = y / noiseScale;
            double noiseValue = noise.noise(sampleX, sampleY, 0);

            uint8_t colorId = 255 * noiseValue;
            sf::Color color(colorId, colorId, colorId);
            map.image.setPixel(x, y, color);
        }
    }

    map.texture.update(map.image);
    map.sprite.setTexture(map.texture);
}

void updateSlider(tg::Slider::Ptr slider, const tg::String newText)
{
    double newValue = newText.toFloat(1);
    slider->setValue(newValue);
    regenerateNoise(map, newValue);
}

void updateBox(tg::EditBox::Ptr box, double newValue)
{
    box->setText(std::to_string(newValue));
    regenerateNoise(map, newValue);
}

void createWidgets(tg::GuiSFML &gui, NoiseMap &map)
{
    tg::Panel::Ptr panel = tg::Panel::create();
    panel->setPosition(500, 0);
    panel->setSize(250, 500);
    panel->getSharedRenderer()->setBackgroundColor(BLACK);

    tg::Label::Ptr scaleLabel = tg::Label::create();
    scaleLabel->setText("Noise Scale");
    scaleLabel->setPosition(10, 10);
    scaleLabel->setSize(110, 20);
    scaleLabel->getSharedRenderer()->setTextColor(WHITE);
    scaleLabel->setHorizontalAlignment(tg::Label::HorizontalAlignment::Center);
    scaleLabel->setVerticalAlignment(tg::Label::VerticalAlignment::Center);
    panel->add(scaleLabel);

    tg::EditBox::Ptr scaleBox = tg::EditBox::create();
    scaleBox->setText(std::to_string(DEFAULT_NOISE_SCALE));
    scaleBox->setPosition(130, 10);
    scaleBox->setSize(110, 20);

    tg::Slider::Ptr scaleSlider = tg::Slider::create();
    scaleSlider->setPosition(10, 40);
    scaleSlider->setSize(230, 20);
    scaleSlider->setMinimum(MIN_NOISE_SCALE);
    scaleSlider->setMaximum(MAX_NOISE_SCALE);
    scaleSlider->setValue(DEFAULT_NOISE_SCALE);
    scaleSlider->setStep(0.001);

    scaleBox->onReturnOrUnfocus(&updateSlider, scaleSlider);
    scaleSlider->onValueChange(&updateBox, scaleBox);

    panel->add(scaleBox, "scaleBox");
    panel->add(scaleSlider);

    gui.add(panel);
}

int main()
{
    sf::RenderWindow window(sf::VideoMode(750, 500), "Noise Visualizer");

    tg::GuiSFML gui;
    gui.setTarget(window);
    gui.setTextSize(12);
    createWidgets(gui, map);

    map.image.create(MAP_WIDTH, MAP_HEIGHT);
    map.texture.loadFromImage(map.image);
    map.sprite.setTexture(map.texture);
    map.sprite.setScale(2, 2);

    regenerateNoise(map, DEFAULT_NOISE_SCALE);

    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            gui.handleEvent(event);
            if (event.type == sf::Event::Closed)
            {
                window.close();
            }
        }

        tg::EditBox::Ptr box = gui.get<tg::EditBox>("scaleBox");

        window.clear(BLACK);
        window.draw(map.sprite);
        gui.draw();
        window.display();
    }

    return 0;
}

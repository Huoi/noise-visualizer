#include <SFML/Graphics.hpp>
#include <TGUI/TGUI.hpp>
#include <TGUI/Backend/SFML-Graphics.hpp>

#include "PerlinNoise.hpp"

#include <cstdint>
#include <iostream>
#include <limits>
#include <random>
#include <string>
#include <vector>

const unsigned int SIZES[6] = {50, 100, 125, 200, 250, 500};
#define DEFAULT_SIZE_ID 5

#define MIN_SEED 0
#define MAX_SEED 4294967295
#define DEFAULT_SEED 0

#define MIN_SCALE 1.0
#define MAX_SCALE 100.0
#define DEFAULT_SCALE 10.0

#define MIN_OCTAVES 1
#define MAX_OCTAVES 10
#define DEFAULT_OCTAVES 1

#define MIN_PERSISTENCE 0.1
#define MAX_PERSISTENCE 1.0
#define DEFAULT_PERSISTENCE 0.1

#define MIN_LACUNARITY 1.0
#define MAX_LACUNARITY 10.0
#define DEFAULT_LACUNARITY 2

#define MAX_OFFSET 50
#define MIN_OFFSET -50
#define DEFAULT_OFFSET_X 0
#define DEFAULT_OFFSET_Y 0

namespace tg = tgui;

struct NoiseMap
{
    sf::Image image;
    sf::Texture texture;
    sf::Sprite sprite;

    unsigned int size;
    unsigned int seed;
    double scale;
    unsigned int octaves;
    double persistence;
    double lacunarity;
    double offsetX;
    double offsetY;

    double noiseMap[500][500];
};

NoiseMap map;

double inverseLerp(double a, double b, double t)
{
    return (t - a) / (b - a);
}

void regenerateNoise()
{
    PerlinNoise noise(map.seed);

    map.image.create(map.size, map.size);
    double scale = 500.0 / map.size;
    map.sprite.setScale(scale, scale);

    double minNoise = std::numeric_limits<double>::max();
    double maxNoise = std::numeric_limits<double>::min();

    for (unsigned int y = 0; y < map.size; ++y)
    {
        for (unsigned int x = 0; x < map.size; ++x)
        {
            double amplitude = 1;
            double frequency = 1;
            double noiseValue = 0;

            for (unsigned int i = 0; i < map.octaves; ++i)
            {
                double sampleX = x / map.scale * frequency + map.offsetX;
                double sampleY = y / map.scale * frequency + map.offsetY;

                double perlinValue = noise.noise(sampleX, sampleY, 0) * 2 - 1;
                noiseValue += perlinValue * amplitude;

                amplitude *= map.persistence;
                frequency *= map.lacunarity;
            }

            if (noiseValue > maxNoise)
                maxNoise = noiseValue;
            else if (noiseValue < minNoise)
                minNoise = noiseValue;

            map.noiseMap[x][y] = noiseValue;
        }
    }

    for (unsigned int y = 0; y < map.size; ++y)
    {
        for (unsigned int x = 0; x < map.size; ++x)
        {
            double noiseValue = inverseLerp(minNoise, maxNoise, map.noiseMap[x][y]);
            unsigned int colorId = 255 * noiseValue;
            sf::Color color(colorId, colorId, colorId);
            map.image.setPixel(x, y, color);
        }
    }

    map.texture.update(map.image);
    map.sprite.setTexture(map.texture);
}

void updateSize(unsigned int index)
{
    map.size = SIZES[index];
    regenerateNoise();
}

void updateSeed(const tg::String newText)
{
    unsigned int newSeed = newText.toUInt(DEFAULT_SEED);
    map.seed = newSeed;
    regenerateNoise();
}

void randomSeed(tg::EditBox::Ptr box)
{
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distr(MIN_SEED, MAX_SEED);
    unsigned int newSeed = distr(gen);
    map.seed = newSeed;
    regenerateNoise();
    box->setText(std::to_string(newSeed));
}

void updateScaleSlider(tg::Slider::Ptr slider, const tg::String newText)
{
    double newValue = newText.toFloat(DEFAULT_SCALE);
    map.scale = newValue;
    regenerateNoise();
    slider->setValue(newValue);
}

void updateScaleBox(tg::EditBox::Ptr box, double newValue)
{
    map.scale = newValue;
    regenerateNoise();
    box->setText(std::to_string(newValue));
}

void updateOctavesSlider(tg::Slider::Ptr slider, const tg::String newText)
{
    double newValue = newText.toUInt(DEFAULT_OCTAVES);
    map.octaves = newValue;
    regenerateNoise();
    slider->setValue(newValue);
}

void updateOctavesBox(tg::EditBox::Ptr box, double newValue)
{
    map.octaves = newValue;
    regenerateNoise();
    box->setText(std::to_string(newValue));
}

void updatePersistenceSlider(tg::Slider::Ptr slider, const tg::String newText)
{
    double newValue = newText.toFloat(DEFAULT_PERSISTENCE);
    map.persistence = newValue;
    regenerateNoise();
    slider->setValue(newValue);
}

void updatePersistenceBox(tg::EditBox::Ptr box, double newValue)
{
    map.persistence = newValue;
    regenerateNoise();
    box->setText(std::to_string(newValue));
}

void updateLacunaritySlider(tg::Slider::Ptr slider, const tg::String newText)
{
    double newValue = newText.toFloat(DEFAULT_LACUNARITY);
    map.lacunarity = newValue;
    regenerateNoise();
    slider->setValue(newValue);
}

void updateLacunarityBox(tg::EditBox::Ptr box, double newValue)
{
    map.lacunarity = newValue;
    regenerateNoise();
    box->setText(std::to_string(newValue));
}

void updateOffsetXSlider(tg::Slider::Ptr slider, const tg::String newText)
{
    double newValue = newText.toFloat(DEFAULT_OFFSET_X);
    map.offsetX = newValue;
    regenerateNoise();
    slider->setValue(newValue);
}

void updateOffsetXBox(tg::EditBox::Ptr box, double newValue)
{
    map.offsetX = newValue;
    regenerateNoise();
    box->setText(std::to_string(newValue));
}

void updateOffsetYSlider(tg::Slider::Ptr slider, const tg::String newText)
{
    double newValue = newText.toFloat(DEFAULT_OFFSET_Y);
    map.offsetY = newValue;
    regenerateNoise();
    slider->setValue(newValue);
}

void updateOffsetYBox(tg::EditBox::Ptr box, double newValue)
{
    map.offsetY = newValue;
    regenerateNoise();
    box->setText(std::to_string(newValue));
}

void createWidgets(tg::BackendGuiSFML &gui)
{
    tg::Panel::Ptr panel = tg::Panel::create();
    panel->setPosition(500, 0);
    panel->setSize(250, 500);
    panel->getSharedRenderer()->setBackgroundColor(sf::Color::Black);

    tg::Label::Ptr sizeLabel = tg::Label::create();
    sizeLabel->setText("Map size");
    sizeLabel->setPosition(10, 10);
    sizeLabel->setSize(110, 20);
    sizeLabel->getSharedRenderer()->setTextColor(sf::Color::White);
    sizeLabel->setHorizontalAlignment(tg::Label::HorizontalAlignment::Left);
    sizeLabel->setVerticalAlignment(tg::Label::VerticalAlignment::Center);
    panel->add(sizeLabel);

    tg::ComboBox::Ptr sizeBox = tg::ComboBox::create();
    sizeBox->setPosition(130, 10);
    sizeBox->setSize(110, 20);
    for (unsigned int i = 0; i < sizeof(SIZES) / sizeof(SIZES[0]); ++i)
    {
        sizeBox->addItem(std::to_string(SIZES[i]));
    }
    sizeBox->setSelectedItemByIndex(DEFAULT_SIZE_ID);
    panel->add(sizeBox);

    tg::Label::Ptr seedLabel = tg::Label::create();
    seedLabel->setText("Seed");
    seedLabel->setPosition(10, 40);
    seedLabel->setSize(110, 20);
    seedLabel->getSharedRenderer()->setTextColor(sf::Color::White);
    seedLabel->setHorizontalAlignment(tg::Label::HorizontalAlignment::Left);
    seedLabel->setVerticalAlignment(tg::Label::VerticalAlignment::Center);
    panel->add(seedLabel);

    tg::EditBox::Ptr seedBox = tg::EditBox::create();
    seedBox->setText(std::to_string(DEFAULT_SEED));
    seedBox->setPosition(130, 40);
    seedBox->setSize(110, 20);
    panel->add(seedBox);

    tg::Button::Ptr seedBtn = tg::Button::create();
    seedBtn->setText("Random seed");
    seedBtn->setPosition(10, 70);
    seedBtn->setSize(230, 20);
    panel->add(seedBtn);

    tg::Label::Ptr scaleLabel = tg::Label::create();
    scaleLabel->setText("Noise Scale");
    scaleLabel->setPosition(10, 100);
    scaleLabel->setSize(110, 20);
    scaleLabel->getSharedRenderer()->setTextColor(sf::Color::White);
    scaleLabel->setHorizontalAlignment(tg::Label::HorizontalAlignment::Left);
    scaleLabel->setVerticalAlignment(tg::Label::VerticalAlignment::Center);
    panel->add(scaleLabel);

    tg::EditBox::Ptr scaleBox = tg::EditBox::create();
    scaleBox->setText(std::to_string(DEFAULT_SCALE));
    scaleBox->setPosition(130, 100);
    scaleBox->setSize(110, 20);
    panel->add(scaleBox);

    tg::Slider::Ptr scaleSlider = tg::Slider::create();
    scaleSlider->setPosition(10, 130);
    scaleSlider->setSize(230, 20);
    scaleSlider->setMinimum(MIN_SCALE);
    scaleSlider->setMaximum(MAX_SCALE);
    scaleSlider->setValue(DEFAULT_SCALE);
    scaleSlider->setStep(0.001);
    panel->add(scaleSlider);

    tg::Label::Ptr octavesLabel = tg::Label::create();
    octavesLabel->setText("Octaves");
    octavesLabel->setPosition(10, 160);
    octavesLabel->setSize(110, 20);
    octavesLabel->getSharedRenderer()->setTextColor(sf::Color::White);
    octavesLabel->setHorizontalAlignment(tg::Label::HorizontalAlignment::Left);
    octavesLabel->setVerticalAlignment(tg::Label::VerticalAlignment::Center);
    panel->add(octavesLabel);

    tg::EditBox::Ptr octavesBox = tg::EditBox::create();
    octavesBox->setText(std::to_string(DEFAULT_OCTAVES));
    octavesBox->setPosition(130, 160);
    octavesBox->setSize(110, 20);
    panel->add(octavesBox);

    tg::Slider::Ptr octavesSlider = tg::Slider::create();
    octavesSlider->setPosition(10, 190);
    octavesSlider->setSize(230, 20);
    octavesSlider->setMinimum(MIN_OCTAVES);
    octavesSlider->setMaximum(MAX_OCTAVES);
    octavesSlider->setValue(DEFAULT_OCTAVES);
    octavesSlider->setStep(1);
    panel->add(octavesSlider);

    tg::Label::Ptr persistenceLabel = tg::Label::create();
    persistenceLabel->setText("Persistence");
    persistenceLabel->setPosition(10, 220);
    persistenceLabel->setSize(110, 20);
    persistenceLabel->getSharedRenderer()->setTextColor(sf::Color::White);
    persistenceLabel->setHorizontalAlignment(tg::Label::HorizontalAlignment::Left);
    persistenceLabel->setVerticalAlignment(tg::Label::VerticalAlignment::Center);
    panel->add(persistenceLabel);

    tg::EditBox::Ptr persistenceBox = tg::EditBox::create();
    persistenceBox->setText(std::to_string(DEFAULT_PERSISTENCE));
    persistenceBox->setPosition(130, 220);
    persistenceBox->setSize(110, 20);
    panel->add(persistenceBox);

    tg::Slider::Ptr persistenceSlider = tg::Slider::create();
    persistenceSlider->setPosition(10, 250);
    persistenceSlider->setSize(230, 20);
    persistenceSlider->setMinimum(MIN_PERSISTENCE);
    persistenceSlider->setMaximum(MAX_PERSISTENCE);
    persistenceSlider->setValue(DEFAULT_PERSISTENCE);
    persistenceSlider->setStep(0.001);
    panel->add(persistenceSlider);

    tg::Label::Ptr lacunarityLabel = tg::Label::create();
    lacunarityLabel->setText("Lacunarity");
    lacunarityLabel->setPosition(10, 280);
    lacunarityLabel->setSize(110, 20);
    lacunarityLabel->getSharedRenderer()->setTextColor(sf::Color::White);
    lacunarityLabel->setHorizontalAlignment(tg::Label::HorizontalAlignment::Left);
    lacunarityLabel->setVerticalAlignment(tg::Label::VerticalAlignment::Center);
    panel->add(lacunarityLabel);

    tg::EditBox::Ptr lacunarityBox = tg::EditBox::create();
    lacunarityBox->setText(std::to_string(DEFAULT_LACUNARITY));
    lacunarityBox->setPosition(130, 280);
    lacunarityBox->setSize(110, 20);
    panel->add(lacunarityBox);

    tg::Slider::Ptr lacunaritySlider = tg::Slider::create();
    lacunaritySlider->setPosition(10, 310);
    lacunaritySlider->setSize(230, 20);
    lacunaritySlider->setMinimum(MIN_LACUNARITY);
    lacunaritySlider->setMaximum(MAX_LACUNARITY);
    lacunaritySlider->setValue(DEFAULT_LACUNARITY);
    lacunaritySlider->setStep(0.001);
    panel->add(lacunaritySlider);

    tg::Label::Ptr offsetXLabel = tg::Label::create();
    offsetXLabel->setText("Offset X");
    offsetXLabel->setPosition(10, 340);
    offsetXLabel->setSize(110, 20);
    offsetXLabel->getSharedRenderer()->setTextColor(sf::Color::White);
    offsetXLabel->setHorizontalAlignment(tg::Label::HorizontalAlignment::Left);
    offsetXLabel->setVerticalAlignment(tg::Label::VerticalAlignment::Center);
    panel->add(offsetXLabel);

    tg::EditBox::Ptr offsetXBox = tg::EditBox::create();
    offsetXBox->setText(std::to_string(DEFAULT_OFFSET_X));
    offsetXBox->setPosition(130, 340);
    offsetXBox->setSize(110, 20);
    panel->add(offsetXBox);

    tg::Slider::Ptr offsetXSlider = tg::Slider::create();
    offsetXSlider->setPosition(10, 370);
    offsetXSlider->setSize(230, 20);
    offsetXSlider->setMinimum(MIN_OFFSET);
    offsetXSlider->setMaximum(MAX_OFFSET);
    offsetXSlider->setValue(DEFAULT_OFFSET_X);
    offsetXSlider->setStep(0.001);
    panel->add(offsetXSlider);

    tg::Label::Ptr offsetYLabel = tg::Label::create();
    offsetYLabel->setText("Offset Y");
    offsetYLabel->setPosition(10, 400);
    offsetYLabel->setSize(110, 20);
    offsetYLabel->getSharedRenderer()->setTextColor(sf::Color::White);
    offsetYLabel->setHorizontalAlignment(tg::Label::HorizontalAlignment::Left);
    offsetYLabel->setVerticalAlignment(tg::Label::VerticalAlignment::Center);
    panel->add(offsetYLabel);

    tg::EditBox::Ptr offsetYBox = tg::EditBox::create();
    offsetYBox->setText(std::to_string(DEFAULT_OFFSET_Y));
    offsetYBox->setPosition(130, 400);
    offsetYBox->setSize(110, 20);
    panel->add(offsetYBox);

    tg::Slider::Ptr offsetYSlider = tg::Slider::create();
    offsetYSlider->setPosition(10, 430);
    offsetYSlider->setSize(230, 20);
    offsetYSlider->setMinimum(MIN_OFFSET);
    offsetYSlider->setMaximum(MAX_OFFSET);
    offsetYSlider->setValue(DEFAULT_OFFSET_Y);
    offsetYSlider->setStep(0.001);
    panel->add(offsetYSlider);

    tg::Button::Ptr regenerateBtn = tg::Button::create();
    regenerateBtn->setText("Regenerate Noise");
    regenerateBtn->setPosition(10, 460);
    regenerateBtn->setSize(230, 20);
    panel->add(regenerateBtn);

    sizeBox->onItemSelect(&updateSize);

    seedBox->onReturnOrUnfocus(&updateSeed);
    seedBtn->onPress(&randomSeed, seedBox);

    scaleBox->onReturnOrUnfocus(&updateScaleSlider, scaleSlider);
    scaleSlider->onValueChange(&updateScaleBox, scaleBox);

    octavesBox->onReturnOrUnfocus(&updateOctavesSlider, octavesSlider);
    octavesSlider->onValueChange(&updateOctavesBox, octavesBox);

    persistenceBox->onReturnOrUnfocus(&updatePersistenceSlider, persistenceSlider);
    persistenceSlider->onValueChange(&updatePersistenceBox, persistenceBox);

    lacunarityBox->onReturnOrUnfocus(&updateLacunaritySlider, lacunaritySlider);
    lacunaritySlider->onValueChange(&updateLacunarityBox, lacunarityBox);

    offsetXBox->onReturnOrUnfocus(&updateOffsetXSlider, offsetXSlider);
    offsetXSlider->onValueChange(&updateOffsetXBox, offsetXBox);

    offsetYBox->onReturnOrUnfocus(&updateOffsetYSlider, offsetYSlider);
    offsetYSlider->onValueChange(&updateOffsetYBox, offsetYBox);

    regenerateBtn->onPress(&regenerateNoise);

    gui.add(panel);
}

int main()
{
    sf::RenderWindow window(sf::VideoMode(750, 500), "Noise Visualizer");

    tg::Gui gui;
    gui.setTarget(window);
    gui.setTextSize(12);
    createWidgets(gui);

    map.image.create(SIZES[DEFAULT_SIZE_ID], SIZES[DEFAULT_SIZE_ID]);
    map.texture.loadFromImage(map.image);
    map.sprite.setTexture(map.texture);
    double scale = 500 / SIZES[DEFAULT_SIZE_ID];
    map.sprite.setScale(scale, scale);

    map.size = SIZES[DEFAULT_SIZE_ID];
    map.seed = DEFAULT_SEED;
    map.scale = DEFAULT_SCALE;
    map.octaves = DEFAULT_OCTAVES;
    map.persistence = DEFAULT_PERSISTENCE;
    map.lacunarity = DEFAULT_LACUNARITY;
    map.offsetX = DEFAULT_OFFSET_X;
    map.offsetY = DEFAULT_OFFSET_Y;

    regenerateNoise();

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

        window.clear(sf::Color::White);
        window.draw(map.sprite);
        gui.draw();
        window.display();
    }

    return 0;
}

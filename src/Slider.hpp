#ifndef SLIDER_H
#define SLIDER_H

#include <SFML/Graphics.hpp>
#include <cstdint>

class Slider
{
public:
    Slider(const uint16_t axisX,
           const uint16_t axisY,
           const uint16_t axisW,
           const uint16_t axisH,
           const uint16_t handleW,
           const uint16_t handleH,
           const double minValue,
           const double maxValue,
           const double defaultValue,
           const sf::Color axisColor = sf::Color::Red,
           const sf::Color handleColor = sf::Color(255, 255, 255, 100));

    double getValue();
    bool valueChanged();
    void logic(sf::RenderWindow &window);
    void draw(sf::RenderWindow &window);

private:
    uint16_t m_axisX;
    uint16_t m_axisY;
    uint16_t m_axisW;
    uint16_t m_axisH;

    uint16_t m_handleW;
    uint16_t m_handleH;

    double m_minValue;
    double m_maxValue;
    double m_currentValue;

    sf::RectangleShape m_axis;
    sf::RectangleShape m_handle;

    bool m_valueChanged;
};

#endif

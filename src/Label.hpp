#ifndef LABEL_H
#define LABEL_H

#include <SFML/Graphics.hpp>

#include <cstdint>
#include <string>

class Label
{
public:
    Label(const uint16_t x,
          const uint16_t y,
          const std::string text,
          const sf::Font &font,
          const uint8_t fontSize,
          const sf::Color fontColor = sf::Color::Black);

    void setText(const std::string text);
    void draw(sf::RenderWindow &window);

private:
    sf::Text label;
};

#endif

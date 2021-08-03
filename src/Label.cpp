#include <SFML/Graphics.hpp>

#include "Label.hpp"

Label::Label(const uint16_t x,
             const uint16_t y,
             const std::string text,
             const sf::Font &font,
             const uint8_t fontSize,
             const sf::Color fontColor)
{
    label.setFont(font);
    label.setString(text);
    label.setCharacterSize(fontSize);
    label.setFillColor(fontColor);
    label.setStyle(sf::Text::Regular);
    label.setPosition(x, y);
}

void Label::setText(const std::string text)
{
    label.setString(text);
}

void Label::draw(sf::RenderWindow &window)
{
    window.draw(label);
}

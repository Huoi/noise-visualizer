#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>
#include <SFML/Window.hpp>

#include "Slider.hpp"

#include <iostream>

Slider::Slider(const uint16_t axisX,
               const uint16_t axisY,
               const uint16_t axisW,
               const uint16_t axisH,
               const uint16_t handleW,
               const uint16_t handleH,
               const double minValue,
               const double maxValue,
               const double defaultValue,
               const sf::Color axisColor,
               const sf::Color handleColor)
{
    m_axisX = axisX;
    m_axisY = axisY;
    m_axisW = axisW;
    m_axisH = axisH;

    m_handleW = handleW;
    m_handleH = handleH;

    m_minValue = minValue;
    m_maxValue = maxValue;
    m_currentValue = defaultValue;

    m_axis.setOrigin(0, m_axisH / 2);
    m_axis.setPosition(m_axisX, m_axisY);
    m_axis.setSize(sf::Vector2f(m_axisW, m_axisH));
    m_axis.setFillColor(axisColor);

    m_handle.setOrigin(m_handleW / 2, m_handleH / 2);
    m_handle.setPosition(m_axisX + m_axisW * (m_currentValue - m_minValue) / (m_maxValue - m_minValue), m_axisY);
    m_handle.setSize(sf::Vector2f(m_handleW, m_handleH));
    m_handle.setFillColor(handleColor);
}

double Slider::getValue()
{
    return m_currentValue;
}

bool Slider::valueChanged()
{
    return m_valueChanged;
}

void Slider::logic(sf::RenderWindow &window)
{
    sf::Vector2i mousePos = sf::Mouse::getPosition(window);
    sf::Vector2f rectPos = m_axis.getPosition();
    sf::Vector2f rectSize = m_axis.getSize();
    // Check mouse collisions with the handle
    if (m_handle.getGlobalBounds().contains(mousePos.x, mousePos.y))
    {
        // Check mouse is pressed
        if (sf::Mouse::isButtonPressed(sf::Mouse::Button::Left))
        {
            // Check mouse is in bounds with axis
            if (mousePos.x >= m_axisX && mousePos.x <= m_axisX + m_axisW)
            {
                m_handle.setPosition(mousePos.x, m_axisY);
                m_currentValue = m_minValue + (m_handle.getPosition().x - m_axisX) / m_axisW * (m_maxValue - m_minValue);
                m_valueChanged = true;
            }
            else
            {
                m_valueChanged = false;
            }
        }
        else
        {
            m_valueChanged = false;
        }
    }
    else
    {
        m_valueChanged = false;
    }
}

void Slider::draw(sf::RenderWindow &window)
{
    logic(window);
    window.draw(m_axis);
    window.draw(m_handle);
}

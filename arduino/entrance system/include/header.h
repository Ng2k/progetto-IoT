#ifndef HEADER_H
#define HEADER_H

#include <Arduino.h> 

// Stati del sensore.
enum class Reading { Read, Idle };

/**
 * @enum Output
 * @brief Stati di output per controllare l'attuatore (LED RGB).
 */
enum class Output { Off, Enter, Exit, Error };
#endif //HEADER_H
// PIC16F877A Configuration Bit Settings

// 'C' source line config statements

#include <xc.h>

// #pragma config statements should precede project file includes.
// Use project enums instead of #define for ON and OFF.

// CONFIG
#pragma config FOSC = HS        // Oscillator Selection bits (HS oscillator)
#pragma config WDTE = OFF       // Watchdog Timer Enable bit (WDT disabled)
#pragma config PWRTE = OFF      // Power-up Timer Enable bit (PWRT disabled)
#pragma config BOREN = ON       // Brown-out Reset Enable bit (BOR enabled)
#pragma config LVP = ON         // Low-Voltage (Single-Supply) In-Circuit Serial Programming Enable bit (RB3/PGM pin has PGM function; low-voltage programming enabled)
#pragma config CPD = OFF        // Data EEPROM Memory Code Protection bit (Data EEPROM code protection off)
#pragma config WRT = OFF        // Flash Program Memory Write Enable bits (Write protection off; all program memory may be written to by EECON control)
#pragma config CP = OFF         // Flash Program Memory Code Protection bit (Code protection off)

char ch;

#define _XTAL_FREQ 20000000

void uart_init()
{
    TXEN = 1; 
    BRGH = 1;
    SPEN = 1;
    CREN = 1;
    SPBRG = 129;
    
    GIE = 1;
    PEIE = 1;
    RCIF = 0;
    RCIE = 1;
}


void interrupt ISR()
{
    if(RCIF)
    {
        RCIF = 0;
        
        ch = RCREG;
        
        TRMT = 0;
        TXREG = ch;
        while(!TRMT);
    }
}

void uart_tx_char(char ch)
{
    TRMT = 0;
    TXREG = ch;
    while(!TRMT);
}

void main(void) {
    uart_init();
    char ch = 'a';
    while(1)
    {
        /*
        uart_tx_char(ch++);
        
        if(ch=='z')
        {
            uart_tx_char('\n');
            uart_tx_char('\r');
            ch = 'a';
        }
         */
    }
    return;
}

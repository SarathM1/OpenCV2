// PIC16F877A Configuration Bit Settings

// 'C' source line config statements

#include <xc.h>

// #pragma config statements should precede project file includes.
// Use project enums instead of #define for ON and OFF.

// CONFIG
#pragma config FOSC = HS        // Oscillator Selection bits (HS oscillator)
#pragma config WDTE = OFF       // Watchdog Timer Enable bit (WDT disabled)
#pragma config PWRTE = OFF      // Power-up Timer Enable bit (PWRT disabled)
#pragma config BOREN = OFF       // Brown-out Reset Enable bit (BOR enabled)
#pragma config LVP = OFF         // Low-Voltage (Single-Supply) In-Circuit Serial Programming Enable bit (RB3/PGM pin has PGM function; low-voltage programming enabled)
#pragma config CPD = OFF        // Data EEPROM Memory Code Protection bit (Data EEPROM code protection off)
#pragma config WRT = OFF        // Flash Program Memory Write Enable bits (Write protection off; all program memory may be written to by EECON control)
#pragma config CP = OFF         // Flash Program Memory Code Protection bit (Code protection off)

char ch;

#define C1B RB7
#define C1A RB6
#define C2B RB5
#define C2A RB4
#define EN1 RB3
#define EN2 RB2

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

void start()
{
  EN2 = 1;   
  EN1 = 1;   
}

void turn_left()
{
  //start();
  C1A = 0;   
  C1B = 0;   
  C2A = 0;   
  C2B = 1;  
}

void turn_right()
{
  ////start();
  C1A = 0;   
  C1B = 0;
  C2A = 1;  
  C2B = 0;   
}

void fwd()
{
  //start();
  C1A = 0;   
  C1B = 1;  
  C2A = 0;   
  C2B = 1;  
}

void back()
{
  //start();
  C1A = 1;  
  C1B = 0;   
  C2A = 1;  
  C2B = 0;   
}

void Stop()
{ 
    
  //EN1 = 0;   
  //EN2 = 0;
  C1A = 0;  
  C1B = 0;   
  C2A = 0;  
  C2B = 0;
}

void uart_tx_char(char ch)
{
    TRMT = 0;
    TXREG = ch;
    while(!TRMT);
}

void interrupt ISR()
{
    if(RCIF)
    {
        RCIF = 0;
        
        ch = RCREG;
        uart_tx_char(ch);
        
        switch(ch)
        {
          case 'l':
                  turn_left();
                  __delay_ms(10);    
                  Stop();
                  break;
          case 'r':
                  turn_right();
                  __delay_ms(10);    
                  Stop();
                  break;

          case 'f':
                  fwd();
                  __delay_ms(10);    
                  Stop();
                  break;
          case 'b':
                  back();
                  __delay_ms(10);    
                  Stop();
                  break;
          default:
                  Stop();
                  break;
        }
    }
}
void main(void) {
    uart_init();
    nRBPU = 1;
    TRISB = 0;
    PORTB = 0;
    start();
    while(1);
    return;
}

/*
 * SMSignals.hpp
 *
 *  Created on: Thursday, 06 January 2022
 *  Author:     watney
 *
 */
#ifndef SMEVENTS_HPP_
#define SMEVENTS_HPP_

typedef unsigned char U8;
typedef unsigned int U32;
typedef int NATIVE_INT_TYPE;

namespace Fw {
class SMSignals {


public:

    enum {
        SERIALIZED_SIZE =
        sizeof(U32) +
        sizeof(U8)*128
    }; //!< serializable size of SMSignals

    SMSignals() {
        this->m_eventSignal = 0;
        for (NATIVE_INT_TYPE _mem = 0; _mem < 128; _mem++) {
            this->m_payload[_mem] = 0;
        }
    }

    SMSignals(const SMSignals* src); //!< pointer copy constructor
    SMSignals(const SMSignals& src); //!< reference copy constructor
    SMSignals(U32 eventSignal, const U8* payload, NATIVE_INT_TYPE payloadSize); //!< constructor with arguments
    SMSignals(U32 eventSignal, const U8 payload); //!< constructor with arguments with scalars for array arguments
    SMSignals& operator=(const SMSignals& src); //!< equal operator
    bool operator==(const SMSignals& src) const; //!< equality operator

    void set(U32 eventSignal, const U8* payload, NATIVE_INT_TYPE payloadSize); //!< set values

    U32 geteventSignal() const {return m_eventSignal;} //!< get member eventSignal
    const U8* getpayload(NATIVE_INT_TYPE& size) const; //!< get member payload

    void seteventSignal(U32 val) {m_eventSignal = val;} //!< set member eventSignal
    void setpayload(const U8* val, NATIVE_INT_TYPE size); //!< set member payload


protected:

    enum {
        TYPE_ID = 0x2AAA5CFB //!< type id
    };

    U32 m_eventSignal; //<! eventSignal - 
    U8 m_payload[128]; //<! payload - 

private:

};

};
#endif


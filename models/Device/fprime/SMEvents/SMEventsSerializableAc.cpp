#include <SMEvents/SMEventsSerializableAc.hpp>
#include <Fw/Types/Assert.hpp>
#include <Fw/Types/BasicTypes.hpp>
#include <Fw/Types/StringUtils.hpp>
#if FW_SERIALIZABLE_TO_STRING
#include <Fw/Types/String.hpp>
#endif
#include <cstring>
namespace Svc {
// public methods

SMEvents::SMEvents(): Serializable() {
    this->m_eventSignal = 0;
    for (NATIVE_INT_TYPE _mem = 0; _mem < 128; _mem++) {
        this->m_payload[_mem] = 0;
    }
}

SMEvents::SMEvents(const SMEvents& src) : Serializable() {
    this->set(src.m_eventSignal, src.m_payload, 128);
}

SMEvents::SMEvents(const SMEvents* src) : Serializable() {
    FW_ASSERT(src);
    this->set(src->m_eventSignal, src->m_payload, 128);
}

SMEvents::SMEvents(U32 eventSignal, const U8* payload, NATIVE_INT_TYPE payloadSize) : Serializable() {
    this->set(eventSignal, payload, 128);
}

SMEvents::SMEvents(U32 eventSignal, const U8 payload) : Serializable() {
    this->m_eventSignal = eventSignal;
    for (NATIVE_INT_TYPE _mem = 0; _mem < 128; _mem++) {
        this->m_payload[_mem] = payload;
    }
}


SMEvents& SMEvents::operator=(const SMEvents& src) {
    if(this == &src) {
            return *this;
    }

    this->set(src.m_eventSignal, src.m_payload, 128);
    return *this;
}

bool SMEvents::operator==(const SMEvents& src) const {
    return (
        (src.m_eventSignal == this->m_eventSignal) &&
        (src.m_payload == this->m_payload) &&
        true);
}

void SMEvents::set(U32 eventSignal, const U8* payload, NATIVE_INT_TYPE payloadSize) {
    this->m_eventSignal = eventSignal;
    for (NATIVE_INT_TYPE _mem = 0; _mem < FW_MIN(payloadSize,128); _mem++) {
        this->m_payload[_mem] = payload[_mem];
    }
}

U32 SMEvents::geteventSignal() const {
    return this->m_eventSignal;
}

const U8* SMEvents::getpayload(NATIVE_INT_TYPE& size) const {
    size = 128;
    return this->m_payload;
}


void SMEvents::seteventSignal(U32 val) {
    this->m_eventSignal = val;
}
void SMEvents::setpayload(const U8* val, NATIVE_INT_TYPE size) {
    for (NATIVE_INT_TYPE _mem = 0; _mem < FW_MIN(size,128); _mem++) {
        this->m_payload[_mem] = val[_mem];
    }
}
Fw::SerializeStatus SMEvents::serialize(Fw::SerializeBufferBase& buffer) const {
    Fw::SerializeStatus stat;

#if FW_SERIALIZATION_TYPE_ID
    // serialize type ID
    stat = buffer.serialize(static_cast<U32>(SMEvents::TYPE_ID));
#endif

    stat = buffer.serialize(this->m_eventSignal);
    if (stat != Fw::FW_SERIALIZE_OK) {
        return stat;
    }
    for (NATIVE_INT_TYPE _mem = 0; _mem < 128; _mem++) {
        stat = buffer.serialize(this->m_payload[_mem]);
        if (stat != Fw::FW_SERIALIZE_OK) {
            return stat;
        }
    }
    return stat;
}

Fw::SerializeStatus SMEvents::deserialize(Fw::SerializeBufferBase& buffer) {
    Fw::SerializeStatus stat;

#if FW_SERIALIZATION_TYPE_ID
    U32 typeId;

    stat = buffer.deserialize(typeId);
    if (stat != Fw::FW_SERIALIZE_OK) {
        return stat;
    }

    if (typeId != SMEvents::TYPE_ID) {
        return Fw::FW_DESERIALIZE_TYPE_MISMATCH;
    }
#endif

    stat = buffer.deserialize(this->m_eventSignal);
    if (stat != Fw::FW_SERIALIZE_OK) {
        return stat;
    }
    for (NATIVE_INT_TYPE _mem = 0; _mem < 128; _mem++) {
        stat = buffer.deserialize(this->m_payload[_mem]);
        if (stat != Fw::FW_SERIALIZE_OK) {
            return stat;
        }
    }
    return stat;
}

#if FW_SERIALIZABLE_TO_STRING  || BUILD_UT

void SMEvents::toString(Fw::StringBase& text) const {

    static const char * formatString =
       "("
       "eventSignal = %u, "
       "payload = "
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[]"
       "[] "
       ")";

    // declare strings to hold any serializable toString() arguments


    char outputString[FW_SERIALIZABLE_TO_STRING_BUFFER_SIZE];
    (void)snprintf(outputString,FW_SERIALIZABLE_TO_STRING_BUFFER_SIZE,formatString
       ,this->m_eventSignal
       ,this->m_payload[0]
       ,this->m_payload[1]
       ,this->m_payload[2]
       ,this->m_payload[3]
       ,this->m_payload[4]
       ,this->m_payload[5]
       ,this->m_payload[6]
       ,this->m_payload[7]
       ,this->m_payload[8]
       ,this->m_payload[9]
       ,this->m_payload[10]
       ,this->m_payload[11]
       ,this->m_payload[12]
       ,this->m_payload[13]
       ,this->m_payload[14]
       ,this->m_payload[15]
       ,this->m_payload[16]
       ,this->m_payload[17]
       ,this->m_payload[18]
       ,this->m_payload[19]
       ,this->m_payload[20]
       ,this->m_payload[21]
       ,this->m_payload[22]
       ,this->m_payload[23]
       ,this->m_payload[24]
       ,this->m_payload[25]
       ,this->m_payload[26]
       ,this->m_payload[27]
       ,this->m_payload[28]
       ,this->m_payload[29]
       ,this->m_payload[30]
       ,this->m_payload[31]
       ,this->m_payload[32]
       ,this->m_payload[33]
       ,this->m_payload[34]
       ,this->m_payload[35]
       ,this->m_payload[36]
       ,this->m_payload[37]
       ,this->m_payload[38]
       ,this->m_payload[39]
       ,this->m_payload[40]
       ,this->m_payload[41]
       ,this->m_payload[42]
       ,this->m_payload[43]
       ,this->m_payload[44]
       ,this->m_payload[45]
       ,this->m_payload[46]
       ,this->m_payload[47]
       ,this->m_payload[48]
       ,this->m_payload[49]
       ,this->m_payload[50]
       ,this->m_payload[51]
       ,this->m_payload[52]
       ,this->m_payload[53]
       ,this->m_payload[54]
       ,this->m_payload[55]
       ,this->m_payload[56]
       ,this->m_payload[57]
       ,this->m_payload[58]
       ,this->m_payload[59]
       ,this->m_payload[60]
       ,this->m_payload[61]
       ,this->m_payload[62]
       ,this->m_payload[63]
       ,this->m_payload[64]
       ,this->m_payload[65]
       ,this->m_payload[66]
       ,this->m_payload[67]
       ,this->m_payload[68]
       ,this->m_payload[69]
       ,this->m_payload[70]
       ,this->m_payload[71]
       ,this->m_payload[72]
       ,this->m_payload[73]
       ,this->m_payload[74]
       ,this->m_payload[75]
       ,this->m_payload[76]
       ,this->m_payload[77]
       ,this->m_payload[78]
       ,this->m_payload[79]
       ,this->m_payload[80]
       ,this->m_payload[81]
       ,this->m_payload[82]
       ,this->m_payload[83]
       ,this->m_payload[84]
       ,this->m_payload[85]
       ,this->m_payload[86]
       ,this->m_payload[87]
       ,this->m_payload[88]
       ,this->m_payload[89]
       ,this->m_payload[90]
       ,this->m_payload[91]
       ,this->m_payload[92]
       ,this->m_payload[93]
       ,this->m_payload[94]
       ,this->m_payload[95]
       ,this->m_payload[96]
       ,this->m_payload[97]
       ,this->m_payload[98]
       ,this->m_payload[99]
       ,this->m_payload[100]
       ,this->m_payload[101]
       ,this->m_payload[102]
       ,this->m_payload[103]
       ,this->m_payload[104]
       ,this->m_payload[105]
       ,this->m_payload[106]
       ,this->m_payload[107]
       ,this->m_payload[108]
       ,this->m_payload[109]
       ,this->m_payload[110]
       ,this->m_payload[111]
       ,this->m_payload[112]
       ,this->m_payload[113]
       ,this->m_payload[114]
       ,this->m_payload[115]
       ,this->m_payload[116]
       ,this->m_payload[117]
       ,this->m_payload[118]
       ,this->m_payload[119]
       ,this->m_payload[120]
       ,this->m_payload[121]
       ,this->m_payload[122]
       ,this->m_payload[123]
       ,this->m_payload[124]
       ,this->m_payload[125]
       ,this->m_payload[126]
       ,this->m_payload[127]
    );
    outputString[FW_SERIALIZABLE_TO_STRING_BUFFER_SIZE-1] = 0; // NULL terminate

    text = outputString;
}

#endif

#ifdef BUILD_UT
    std::ostream& operator<<(std::ostream& os, const SMEvents& obj) {
        Fw::String str;
        obj.toString(str);
        os << str.toChar();
        return os;
    }
#endif
} // end namespace Svc

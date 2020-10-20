#ifndef __VKEXT_TL_PARSE_H__
#define __VKEXT_TL_PARSE_H__

void tl_parse_init();
int tl_parse_int();
long long tl_parse_long();
double tl_parse_double();
float tl_parse_float();
int tl_parse_string(char **s);
int tl_eparse_string(char **s);
char *tl_parse_error();
void tl_set_error(const char *error);
void tl_parse_end();
int tl_parse_save_pos();
int tl_parse_restore_pos(int pos);
void tl_parse_clear_error();
#endif
